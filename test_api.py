import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print('Key starts with:', GEMINI_API_KEY[:5])
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content('Say hello')
    print('Response:', response.text)
except Exception as e:
    print('Error:', e)
