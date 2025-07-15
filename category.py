import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('API_KEY_TURBO')  # Замените на ваш ключ

ALLOWED_CATEGORIES = {'техническая', 'оплата', 'другое'}


def get_complaint_category(text: str) -> str:
    prompt = f'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. Ответ только одним словом.'
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            temperature=0
        )
        answer = response['choices'][0]['message']['content'].strip().lower()

        return answer if answer in ALLOWED_CATEGORIES else 'другое'
    except Exception as exc:
        return 'другое'
