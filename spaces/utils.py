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

        As a fire risk management consultant, give fire prevention tips as specific as possible for the space and fire items.
        give tips **briefly** considering the priority of items to prevent fire in the space.

        [input data structure].
        - Space: {space}
        - Fire items: {fire_items_str}

        [Example of dynamic prompt generation].
        WARNING: make sure to put icons in the prompt to make it easier to read.
        Space: Home
        Fire items: refrigerator, gas stove, electric stove, wood stove, wood boiler, air conditioner
        ;

        🏠 Home Safety: Fire Hazards and Prevention
        🔥 Common Causes of Fire Incidents at Home
        Cooking is frequently a source of fire accidents in homes. 
        It's crucial to be aware of potential risks to prevent these incidents.

        🔍 Your Household Fire Items
        It appears that you have a 🧊 refrigerator, 🍳 gas stove, 🔌 electric stove, 🪵 wood stove, 🌡️ wood boiler, and 🌬️ air conditioner. 
        Among these, the 🍳 gas stove requires the most attention due to its direct use of flames and gas.

        🛠️ Safety Tips for Gas Stove
        Here are a few simple tips to ensure safety when using your gas stove:

        Regularly check for gas leaks.
        Keep flammable materials away from the stove.
        Ensure good ventilation while cooking to prevent gas buildup.
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