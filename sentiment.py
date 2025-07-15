import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Замените на ваш ключ


def analyze_sentiment(text: str) -> str:
    api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == 200:
        result = response.json()
        return result.get('sentiment', 'unknown')
    else:
        raise Exception('Sentiment API unavailable')


