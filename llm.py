import os
from dotenv import load_dotenv

load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GEMINI_KEY'))
def generate_response(feedback):
    model=genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=
            "You are a helpful assistant for a flight branch. Your task is to receive customer feedback about their flight and response to them in a respectful manner."
            "No need to add for more detail from user. If the feedback is an emergency case, tell users to wait for contact from the support team."
            "However, if the customer message is unrelated to any flight aspect, just response 'UNRELATED'"
            )
    response = model.generate_content(feedback)
    return response.text