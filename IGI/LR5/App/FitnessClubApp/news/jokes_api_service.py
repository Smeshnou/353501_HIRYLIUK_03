import requests
from django.core.cache import cache
from django.utils import timezone
from .models import JokeModel

class JokeApiService:
    BASE_URL = "https://official-joke-api.appspot.com"
    
    @staticmethod
    def fetch_and_save_joke(num_joke=1):
        try:
            response = requests.get(f"{JokeApiService.BASE_URL}/jokes/random/{num_joke}", timeout=10)
            response.raise_for_status()
            joke_data = response.json()
            print("API Response:", type(joke_data), joke_data) 
            
            saved_news = []
            for joke in joke_data:
                joke, created = JokeModel.objects.update_or_create(
                    api_id=joke['id'],
                    defaults={
                        'type': joke['type'],
                        'setup': joke['setup'],
                        'punchline': joke['punchline'],
                        'created_at': timezone.now()
                    }
                )
                if created:
                    saved_news.append(joke)
            
            return saved_news
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении новостей: {e}")
            return []