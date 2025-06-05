import requests
from django.core.cache import cache
from django.utils import timezone

class QuoteApiService:
    
    @staticmethod
    def fetch_quote():
        try:
            response = requests.get(f"https://favqs.com/api/qotd", timeout=10)
            response.raise_for_status()
            quote_data = response.json()
            
            return "{}: {}".format(quote_data["quote"]["author"], quote_data["quote"]["body"])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении новостей: {e}")
            return []