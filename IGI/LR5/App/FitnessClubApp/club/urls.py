from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contacts', views.ContactsListView.as_view(), name='contacts'),
    path('policy', views.policy, name='policy'),
    path('faq', views.FAQListView.as_view(), name='faq'),
    path('faq/create', views.FAQCreateView.as_view(), name='create_faq'),
    re_path(r'^faq/delete/(?P<pk>\d+)/$', views.FAQDeleteView.as_view(), name='delete_faq'),
    path('faq/update/<int:pk>/', views.FAQUpdateView.as_view(), name='update_faq'),
    path('vacancy', views.VacancyListView.as_view(), name='vacancy'),
    path('vacancy/create', views.VacancyCreateView.as_view(), name='create_vacancy'),
    re_path(r'^vacancy/delete/(?P<pk>\d+)/$', views.VacancyDeleteView.as_view(), name='delete_vacancy'),
    path('vacancy/update/<int:pk>/', views.VacancyUpdateView.as_view(), name='update_vacancy'),
    path('comments', views.CommentsListView.as_view(), name='comments'),
    path('comments/create', views.CommentsCreateView.as_view(), name='create_comments'),
    path('gym', views.ScheduleListView.as_view(), name='gym'),
    path('gym/booking/<int:pk>', views.BookingCreate, name='book_schedule'),
    path('gym/create', views.GymCreateView.as_view(), name='create_gym'),
    path('schedule/create', views.ScheduleCreateView.as_view(), name='create_schedule'),
]
