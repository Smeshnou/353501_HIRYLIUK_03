from django.shortcuts import render
from .models import Articles
from django.views import generic
from django.views.generic import ListView, View
from django.shortcuts import redirect
from django.urls import reverse
from .models import Articles, JokeModel
from .jokes_api_service import JokeApiService



def news_home(request):
    news_list = Articles.objects.all()
    return render(request, 'news/news_home.html', {"news": news_list})

    

class NewsListView(ListView):
    model = Articles
    template_name = 'news/news_home.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Articles.objects.all().order_by('-created_at')
    
class JokeListView(ListView):
    model = JokeModel
    template_name = 'news/jokes.html'
    context_object_name = 'jokes_list'
    paginate_by = 10
    
    def post(self, request, *args, **kwargs):
        JokeApiService.fetch_and_save_joke()
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return JokeModel.objects.all().order_by('-created_at')
