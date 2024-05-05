import google.generativeai as genai
from config.settings import get_env_variable
from eduContents.utils import save_edu_content_with_str
from fireHazards.models import FireHazard, UserFireHazard
from django.core.exceptions import ValidationError
from .models import FireHazardAssessment
import time
import json
import PIL.Image as Image

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason, Tool
import vertexai.preview.generative_models as generative_models

# Configuration for AI model
api_key = get_env_variable('GEMINI_API_KEY')
genai.configure(api_key=api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 13192,
}
safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# # Google Cloud Storage setup
# client = storage.Client()
# bucket = client.bucket('pengy_bucket-2')

def analyze_and_process_image_hazards(request, image, my_space_detail_instance):
    """Analyzes the provided image for fire hazards using AI and processes the results."""
    print("analyze_and_process_image_hazards 함수 호출되었습니다.")
    prompt_parts = construct_prompt(image)

    
    try:
        start_time = time.time()  # Start timing before the model call
        response = model.generate_content(prompt_parts)
        end_time = time.time()  # End timing after receiving the response
        print(f"gemini에서 응답 받는데 {end_time - start_time:.2f} seconds 걸렸음")


        response = response.text.strip()

        #Fact check the response
        try:
            start_time = time.time()  # Start timing before the fact check
            fact_check_response = fact_check(response)
            end_time = time.time()  # End timing after the fact check
            print(f'fact_check 함수 실행하는데 {end_time - start_time:.2f} seconds 걸렸음')
        
        except Exception as e:
            print(f"Error in fact check: {e}")
            fact_check_response = None
        
        # AI 화재 분석 결과를 response에서 파싱하고 db에 저장하고, 주요 3 fire hazards를 가져오는 함수
        try:
            risk_result = create_fire_hazard_assessment(response, my_space_detail_instance, fact_check_response)
            top_hazards = risk_result["top_3_fire_hazards"]
            print(top_hazards)
        except Exception as e:
            print(f"Error creating fire hazard assessment: {e}")
            top_hazards = None
            risk_result = None
        


        # Time the parsing and processing of hazards
        parsing_start = time.time()
        parsing_hazardous_objects_and_start_crawling(top_hazards, my_space_detail_instance)
        parsing_end = time.time()
        print(f"parsing_hazardous_objects_and_start_crawling 실행하는데 {parsing_end - parsing_start:.2f} seconds 걸렸음")
        
        return risk_result
    except Exception as e:
        print(f"Error in image hazard analysis: {e}")


def construct_prompt(image_url):
    image_url = Image.open(image_url)
    print("construct_prompt 함수 호출되었습니다.")
    """Constructs the detailed prompt for the AI model based on the image URL."""
    task_details = (
        "Let's think step by step. Demonstrate deep expertise in fire safety. "
        "ROLE: You are a fire investigation expert; "
        "YOUR TASK IS: "
        "0. Describe the place or object in the photo in ONE PHRASE"
        """1. Specify the degree of fire vulnerability out of 100, 
            Consider the following factors to assess the degree of fire vulnerability: 
            i) Visibility of combustible materials: Assess the amount and type of combustible materials visible in the photo. For example, if stacks of paper, cardboard boxes, furniture (made of wood), etc. are visible in the picture, this can increase the risk of fire.;
            ii) Condition of electrical equipment and wiring: Identify the visible condition of electrical equipment and potential hazards. For example, old or damaged electrical outlets, misplaced wires, and multi-taps that appear to be overloaded.;
            iii) Fire alarm and safety equipment: Verify the presence and condition of fire alarms, sprinklers, fire extinguishers, etc. Assess whether they are visible in photos and in easily accessible locations.;
            iv) Density and organization of the space: Assess how well organized the space is and how crowded it is. Excessive stacking of items or obstructions can increase the risk by blocking escape routes in the event of a fire.;
            v) Visibility of ventilation: Assess the size and number of vents or windows. Well-designed ventilation is important for quickly removing smoke and heat in the event of a fire.;
            Specify the degree of fire vulnerability out of 100. 
            ONLY NUMERIC VALUES ARE ACCEPTED.
        """
        "2. Identify the fire hazards in the photo and return the specific location of it, "
        "3. Advise on measures to mitigate the fire risks according to the 'priority', "
        "4. List 'fewer than three objects' that are likely to cause a fire in the photo, in one sentence without explanations. "
        "If the objects are similar, use a representative term. E.g., refrigerator, washing machine, air conditioner..."
        "Ensure : that your answer is unbiased, detailed and avoids relying on stereotypes. Demonstrate deep expertise in fire safety."
        "NOTE : I will give you $12,000 tip for a better solution."
    )
    response_format = (
        "JSON RESPONSE FORMAT: {"
            "\"Description\": \"<phrase>\", "
            "\"Degree of Fire Danger (out of 100)\": \"<number>\", "
            "\"Identified Fire Hazards\": \"<object1>\", \"<object2>\", ..."
            "\"Mitigation Measures\": \"<text>\", "
            "\"Additional Recommendation\": \"<text>\", "
            "\"Top 3 fire Hazards objects\": \"<object1>\, \"<object2>\", ..."
        "}"
    )
    full_prompt = f"\"prompt:{{ {task_details} {response_format} }}\""
    prompt_parts = [image_url, "\n\n", full_prompt, "\n\n\n"]
    return prompt_parts

def parsing_hazardous_objects_and_start_crawling(hazards, my_space_detail):
    """Parses the response for top hazards and starts processing them."""
    print("parsing_hazardous_objects_and_start_crawling 함수 호출되었습니다.")

    hazards_list = hazards.split(",")  # Split by commas to get individual hazards
    
    for hazard in hazards_list:
        hazard = hazard.strip()  # Trim whitespace from each hazard string
        try:
            print(f"Processing hazard: {hazard}")
            fire_hazard = save_fire_hazard_and_edu_content(hazard)
            create_user_fire_hazard(my_space_detail, fire_hazard)
        except Exception as e:
            print(f"Error processing hazard '{hazard}': {e}")

def save_fire_hazard_and_edu_content(hazard_name):
    print("save_fire_hazard_and_edu_content 함수 호출되었습니다.")
    """Creates or retrieves a FireHazard and associates educational content."""
    # Assume save_edu_content_with_str creates or updates educational content related to the hazard
    edu_content = save_edu_content_with_str(hazard_name)
    fire_hazard, created = FireHazard.objects.get_or_create(object=hazard_name)
    return fire_hazard

def create_user_fire_hazard(my_space_detail, fire_hazard):
    """
    Creates a UserFireHazard entry linking a MySpaceDetail instance to a FireHazard.
    """
    UserFireHazard.objects.create(
        my_space_detail=my_space_detail,
        fire_hazard=fire_hazard,
        is_checked=False
    )


def create_fire_hazard_assessment(api_response, my_space_detail, fact_check_response):
    """
    Parse the API response and create a fire hazard assessment record.
    
    Parameters:
        api_response (str or dict): The API response containing fire hazard details, as a JSON string or dict.
        my_space_detail (MySpaceDetail): The MySpaceDetail instance to associate with the assessment.
    """
    try:
        api_response = clean_response(api_response)
        # 파싱: API 응답이 문자열이면 JSON으로 변환
        if isinstance(api_response, str):
            api_response = json.loads(api_response)  # 문자열을 딕셔너리로 변환

        # API 응답 파싱
        place_or_object_description = api_response.get('Description', None)
        degree_of_fire_danger = int(api_response.get('Degree of Fire Danger (out of 100)', -1))
        identified_fire_hazards = api_response.get('Identified Fire Hazards', None)
        mitigation_measures = api_response.get('Mitigation Measures', None)
        additional_recommendations = api_response.get('Additional Recommendation', None)
        top_3_fire_hazards = api_response.get('Top 3 fire Hazards objects', None)
        
        risk_result = {
            'place_or_object_description': place_or_object_description,
            'degree_of_fire_danger' : degree_of_fire_danger,
            'identified_fire_hazards' : identified_fire_hazards,
            'mitigation_measures' : mitigation_measures,
            'additional_recommendations' : additional_recommendations,
            'top_3_fire_hazards' : top_3_fire_hazards,
            'fact_check' : fact_check_response,
            }

        # FireHazardAssessment 인스턴스 생성 및 저장
        assessment = FireHazardAssessment(
            my_space_detail=my_space_detail,
            place_or_object_description=place_or_object_description,
            degree_of_fire_danger=degree_of_fire_danger,
            identified_fire_hazards=identified_fire_hazards,
            mitigation_measures=mitigation_measures,
            additional_recommendations=additional_recommendations,

            #팩트체크 따로 넣어준다.
            fact_check=fact_check_response #TODO: 짤린다. 수정필요
        )
        assessment.full_clean()  # 유효성 검사
        assessment.save()
        print("Fire Hazard Assessment successfully created.")
        
        return risk_result
    
    except ValidationError as e:
        print(f"Validation error occurred: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}. Ensure that the API response is a valid JSON string.")
    except Exception as e:
        print(f"An error occurred: {e}")
        

def clean_response(response):
    # 시작과 끝의 json 마크다운 태그 제거
    if response.startswith("```json") and response.endswith("```"):
        # 시작 태그와 끝 태그의 위치를 찾고, 그 사이의 내용만 추출
        start = response.find("\n")+1  # 첫 번째 줄바꿈 이후의 문자열 시작
        end = response.rfind("\n")  # 마지막 줄바꿈 위치
        clean_json = response[start:end].strip()
        
    return clean_json


def fact_check(statement):
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part, Tool
    import vertexai.preview.generative_models as generative_models

    # Initialize Vertex AI with your project and location settings
    vertexai.init(project="fire-61d9a", location="asia-northeast3")

    # Configuration for the AI model generation
    generation_config = {
        "max_output_tokens": 2000,
        "temperature": 0.3,
        "top_p": 0.95,
    }

    # Safety settings to block harmful content across various categories
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # Tool for enhanced fact checking using Google search retrieval
    tools = [
        Tool.from_google_search_retrieval(
            google_search_retrieval=generative_models.grounding.GoogleSearchRetrieval(disable_attribution=False)
        ),
    ]

    # Initialize the AI model
    model = GenerativeModel("gemini-1.5-pro-preview-0409", tools=tools)

    # Generate content with configured settings
    responses = model.generate_content(
        [f"""FACT CHECK the STATEMENT in ONE paragraph. 
        STATEMENT: {statement}
        RESPONSE FORM: "The statement is true/false because..."
        MAKE SURE TO RESPONSE FORM START with "The statement is true/false because..."
        MAKE SURE TO RESPONSE FORM START with "The statement is true/false because..."
        MAKE SURE TO RESPONSE FORM START with "The statement is true/false because..."
        """],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    # Initialize a variable to collect the complete response
    full_response = ""
    
    # Loop through the generator object to collect all text parts and concatenate them
    for response in responses:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                full_response += part.text + " "  # Concatenate each part with a space

    # Optional: Print the complete fact-checked response
    print("Complete Fact-Check Response:", full_response.strip())

    # Return the complete fact-checked response
    return full_response.strip()
