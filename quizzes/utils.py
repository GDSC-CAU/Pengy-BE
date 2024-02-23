# quizzes/utils.py
import google.generativeai as genai
from config.settings import get_env_variable

# API 키 설정
api_key = get_env_variable('GEMINI_API_KEY') # 보안!!!!!
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
def generate_quiz():
    """gemini-pro를 사용해서 화재 O/X 퀴즈를 생성하는 함수"""
    prompt = """
I'm going to create an OX quiz for fire education. You are a firefighting expert and need to make the questions high level, difficult and accurate. 
        The topics should be about fire evacuation, fire common sense, preventing misuse of electrical appliances, and fire carelessness.
        The topics should be randomized and not categorized. The format should be a tuple (question, O or X, and a short answer). 
        Example: 
        1. (In case of a fire, you should use the stairs to evacuate instead of the elevator; O; Elevators are dangerous because they can lose power and smoke in case of a fire).
        2. (All electrical appliances can be extinguished directly with water; X; You should use a dedicated fire extinguisher because using water on an electrical appliance fire poses a risk of electrical shock.)
        Note: (Problem; O or X; brief problem statement) Make sure to follow this format. It must be accurate, difficult, and professional.
    """
    try:
        response = model.generate_content(prompt)
        response = response.text.strip()
    except Exception as e:
        # 예외 처리: 로그 기록, 기본 메시지 반환 등을 여기서 수행
        print(f"Error generating fire prevention tip: {e}")
    print(response)
    return response