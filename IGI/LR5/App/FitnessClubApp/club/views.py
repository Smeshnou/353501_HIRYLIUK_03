from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from users.models import User
from news.news_api_service import NewsApiService
from .models import FAQModel, VacancyModel, CommentsModel, ScheduleModel, GymModel, BookingModel
from .forms import CommentsForm
from django.utils import timezone
from django.contrib import messages

#defaultViews

def index(request):
    return render(request, 'club/home.html', {'news': NewsApiService.fetch_and_save_news(1)[0]})

def about(request):
    return render(request, 'club/about.html')

def policy(request):
    return render(request, 'club/policy.html')

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")

#CommentsViews

class CommentsListView(ListView):
    model = CommentsModel
    template_name = 'club/comments.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average_rating'] = CommentsModel.get_average_rating()
        context['total_reviews'] = CommentsModel.objects.count()
        return context

class CommentsCreateView(LoginRequiredMixin, CreateView):
    model = CommentsModel
    form_class = CommentsForm
    template_name = 'club/comments_create.html'
    success_url = reverse_lazy('comments')
    success_message = "Ваш отзыв успешно добавлен!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

#faqViews

class FAQListView(ListView):
    model = FAQModel
    template_name = 'club/faq.html'
    context_object_name = 'faq_list'
    paginate_by = 10
    
class FAQCreateView(PermissionRequiredMixin, CreateView):
    model = FAQModel
    fields = ['quastion', 'answer']
    template_name = 'club/faq_create.html'
    success_url = reverse_lazy('faq') 
    permission_required = 'club.add_faq'
    
class FAQDeleteView(PermissionRequiredMixin, DeleteView):
    model = FAQModel
    success_url = reverse_lazy('faq')
    permission_required = 'club.delete_faq'
    
class FAQUpdateView(PermissionRequiredMixin, UpdateView):
    model = FAQModel
    fields = ['quastion', 'answer']
    template_name = 'club/faq_update.html'
    success_url = reverse_lazy('faq') 
    permission_required = 'club.change_faq'

#vacancyViews

class VacancyListView(ListView):
    model = VacancyModel
    template_name = 'club/vacancy.html'
    context_object_name = 'vacancy_list'
    paginate_by = 10

class VacancyCreateView(PermissionRequiredMixin, CreateView):
    model = VacancyModel
    fields = ['name', 'description']
    template_name = 'club/vacancy_create.html'
    success_url = reverse_lazy('vacancy') 
    permission_required = 'club.add_vacancy'

class VacancyDeleteView(PermissionRequiredMixin, DeleteView):
    model = VacancyModel
    success_url = reverse_lazy('vacancy')
    permission_required = 'club.delete_vacancy'
    
class VacancyUpdateView(PermissionRequiredMixin, UpdateView):
    model = VacancyModel
    fields = ['name', 'description']
    template_name = 'club/vacancy_update.html'
    success_url = reverse_lazy('vacancy') 
    permission_required = 'club.change_vacancy'

#contactsViews

class ContactsListView(ListView):
    model = User
    template_name = 'club/contacts.html'
    context_object_name = 'contacts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instructors'] = User.objects.filter(role='Instructors') 
        context['admins'] = User.objects.filter(role='Admins')
        return context
    
#SceduleViews

class GymCreateView(PermissionRequiredMixin, CreateView):
    model = GymModel
    fields = ['name', 'description', 'photo']
    template_name = 'club/gym_create.html'
    success_url = reverse_lazy('schedules') 
    permission_required = 'club.add_gym'

class ScheduleCreateView(PermissionRequiredMixin, CreateView):
    model = ScheduleModel
    fields = ['name', 'gym', 'instructor', 'price', 'start_time', 'end_time']
    template_name = 'club/schedule_create.html'
    success_url = reverse_lazy('schedules') 
    permission_required = 'club.add_schedule'

class ScheduleListView(ListView):
    model = ScheduleModel
    template_name = 'club/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            start_time__gte=timezone.now(),
        ).select_related('gym', 'instructor').prefetch_related('users')
        
        if 'gym' in self.request.GET:
            queryset = queryset.filter(gym_id=self.request.GET['gym'])
        
        return queryset.order_by('start_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gyms'] = GymModel.objects.filter()
        return context
   
def BookingCreate(request, pk):
    user = request.user
    schedule = get_object_or_404(ScheduleModel, id=pk)
    if request.POST:
        if BookingModel.objects.filter(user=user, schedule=schedule).exists():
            messages.error(request, 'Вы уже записаны на это занятие!')
            return redirect('gym')
        else:
            if schedule.current_participants >= schedule.max_participants:
                messages.error(request, 'На это занятие нет свободных мест!')
                return redirect('gym')
            else:
                booking = BookingModel.objects.create(
                    user=user,
                    schedule=schedule,
                )
                schedule.save()
                
                messages.success(request, 'Вы успешно записаны на занятие!')
                return redirect('gym')
    return render(request, 'club/book_schedule.html', {'user': user, 'schedule': schedule,})
