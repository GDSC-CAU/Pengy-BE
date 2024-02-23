#spaces/utils.py
import google.generativeai as genai
from config.settings import get_env_variable
from storages.backends.gcloud import GoogleCloudStorage
from datetime import datetime
from django.conf import settings


# API 키 설정
api_key = get_env_variable('GEMINI_API_KEY') # 보안!!!!!
genai.configure(api_key=api_key)

# 모델 초기화
model = genai.GenerativeModel('gemini-pro')

# gemini-pro 모델을 사용하여 화재 예방 팁 생성
def generate_fire_prevention_tips(space, fire_items):
    fire_items_str = ", ".join(fire_items)  # 화재 위험 물품 리스트를 문자열로 변환
    # 프롬프트 전송 및 응답 생성
    prompt = f"""

        As a firefighter, give fire prevention tips as specific as possible for the space and fire items.

        [input data structure].
        - Space: {space}
        - Fire items: {fire_items_str}

        [Example of dynamic prompt generation].
        WARNING: make sure to put icons in the prompt to make it easier to read.
        Space: Movie theater
        Fire items: refrigerator, gas stove, electric stove, wood stove, wood boiler, air conditioner

        ""
        🎥 Fire prevention and response tips for movie theaters 
        Fire prevention and response in large facilities like movie theaters is critical. Movie theaters are a fire hazard because they host large crowds and use a variety of electrical appliances and equipment. 
        Below are specific tips for keeping your movie theater safe, including the list of fire items you provided (refrigerators, gas ranges, electric stoves, wood burning boilers, and air conditioners).

        1. 🧊 Refrigerators and air conditioners.
        - ⚙️ Conduct regular inspections and maintenance to prevent electrical faults or overheating.
        - 🛢️ Regularly check for refrigerant leaks, and manage refrigerant properly as it can contain chemicals that can cause fires.
        - 🧹 Clean the air conditioner filter and the back of the refrigerator regularly to prevent overheating due to dust.

        2. 🔥 Gas stoves and electric stoves.
        - 🚫 The use of gas stoves in the movie theater will be very limited; if used, 🚨 Install gas leak detectors and check them regularly.
        - 🔌 Electric stoves must be turned off and unplugged after use to reduce the risk of electrical fires.
        - 🛡️ Keep combustible materials away from all cooking appliances to prevent the spread of fire in the event of a fire.

        3. 🪵 Firewood boilers
        - 🚫 Wood burning boilers are not commonly used in movie theaters, but if they are, 🌲 keep flammable materials away from the boiler.
        - 🧼 Clean the combustion chamber and flue regularly to prevent soot and debris buildup, which reduces the risk of fire.
        - 🛠️ Use and maintain the boiler as directed by a professional.

        4. 🚒 General fire prevention and response tips.
        - 🚨 Install a sufficient number of smoke detectors and fire extinguishers inside the movie theater and check them regularly.
        - 🚪 Ensure that emergency exits and escape routes are always open, well-marked, and unobstructed.
        - 🛡️ Employees regularly undergo fire response drills to improve their ability to respond in real-life situations.
        - ⚖️ Strictly follow safety regulations for equipment and facilities used in movie theaters, and minimize the use of potentially hazardous items.

        To prevent fires in movie theaters, it's important to adhere to a few key safety practices. 
        Ensure that electrical equipment is routinely inspected and maintained, and keep all areas clean and free of clutter. 
        Safely store any flammable materials, and ensure that fire alarms and extinguishers are in working order and easily accessible.
        By following these simple preventive measures, you can greatly reduce the risk of fire in a movie theater.
        Remember, safety is always the first priority, so stay vigilant!
        ""
    """

    response = model.generate_content(prompt)
    return response.text



# 버킷 이름을 settings에서 가져와야하는데 나중에 바꾸기..
storage = GoogleCloudStorage(bucket_name='pengy_bucket-2')

def upload_image(file, directory):
    try:
        # 파일명을 현재 시각의 타임스탬프로 설정하여 고유하게 만듭니다.
        target_path = f"{directory}/{datetime.now().timestamp()}.jpg"
        # Google Cloud Storage에 파일을 저장하고 저장된 파일의 경로를 반환합니다.
        path = storage.save(target_path, file)
        print(path)
        # 저장된 파일의 URL을 반환합니다.
        return storage.url(path)
    except Exception as e:
        print(e)
        return None