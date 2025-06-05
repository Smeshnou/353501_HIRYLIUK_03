from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_home'),
    path('jokes', views.JokeListView.as_view(), name='jokes'),
]
