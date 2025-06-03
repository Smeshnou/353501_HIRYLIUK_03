import requests
from django.core.cache import cache
from django.utils import timezone
from .models import Articles

class NewsApiService:
    BASE_URL = "https://official-joke-api.appspot.com"
    
    @staticmethod
    def fetch_and_save_news(num_news=1):
        try:
            response = requests.get(f"{NewsApiService.BASE_URL}/jokes/random/{num_news}", timeout=10)
            response.raise_for_status()
            news_data = response.json()
            print("API Response:", type(news_data), news_data) 
            
            saved_news = []
            for news in news_data:
                news, created = Articles.objects.update_or_create(
                    api_id=news['id'],
                    defaults={
                        'type': news['type'],
                        'setup': news['setup'],
                        'punchline': news['punchline'],
                        'created_at': timezone.now()
                    }
                )
                if created:
                    saved_news.append(news)
            
            return saved_news
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении новостей: {e}")
            return []