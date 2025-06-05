from collections import Counter
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from users.models import User
from news.models import Articles
from .models import FAQModel, VacancyModel, CommentsModel, ScheduleModel, GymModel, BookingModel, PromoModel
from .forms import CommentsForm
from django.utils import timezone
from django.contrib import messages
from matplotlib import pyplot as plt
from .quote_api_service import QuoteApiService

#defaultViews

def index(request):
    if(Articles.objects.all()):
        news = Articles.objects.all()[0]
    else:
        news = None
    return render(request, 'club/home.html', {'news': news, 'quote': QuoteApiService.fetch_quote()})

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

    def post(self, request):
        quastion = request.POST.get('quastion')
        answer = request.POST.get('answer')

        FAQModel.objects.create(
            quastion=quastion,
            answer=answer,
            created_at=timezone.now()
        )

        return redirect(self.success_url)

    
class FAQDeleteView(PermissionRequiredMixin, DeleteView):
    model = FAQModel
    success_url = reverse_lazy('faq')
    permission_required = 'club.delete_faq'

    def get(self, request, pk):
        faq = FAQModel.objects.get(pk=pk)
        faq.delete()
        return redirect(self.success_url)
    
    
class FAQUpdateView(PermissionRequiredMixin, UpdateView):
    model = FAQModel
    fields = ['quastion', 'answer', 'created_at']
    template_name = 'club/faq_update.html'
    success_url = reverse_lazy('faq') 
    permission_required = 'club.change_faq'

    def post(self, request, pk):
        faq = FAQModel.objects.get(pk=pk)
        
        faq.quastion = request.POST.get('quastion')
        faq.answer = request.POST.get('answer')
        faq.save()
        
        return redirect(self.success_url)

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
    success_url = reverse_lazy('gym') 
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
   
def BookingCreate(request, pk, promo=None):
    user = request.user
    schedule = get_object_or_404(ScheduleModel, id=pk)

    promo_obj = None
    if promo:
        try:
            promo_obj = PromoModel.objects.get(name=promo)
            if not promo_obj.is_valid():
                messages.error(request, "Промокод недействителен")
                promo_obj = None
        except PromoModel.DoesNotExist:
            return redirect('book_schedule', pk=pk)
        
    if request.POST:
        if BookingModel.objects.filter(user=user, schedule=schedule).exists():
            return redirect('gym')
        else:
            if schedule.current_participants >= schedule.max_participants:
                return redirect('gym')
            else:
                booking = BookingModel.objects.create(
                    user=user,
                    schedule=schedule,
                    promo=promo_obj if promo_obj else None
                )
                booking.save()
                
                return redirect('gym')
    return render(request, 'club/book_schedule.html', {'user': user, 'schedule': schedule, 'promo': promo_obj, 'discounted_price': schedule.get_discounted_price(promo_obj) if promo_obj else None})

def use_promo(request, pk):
    if request.POST:
        promo_code = request.POST.get('promo', '').strip()
        if promo_code:
            return redirect('book_schedule_promo', pk, promo_code)
    return redirect('book_schedule', pk)

def statistics(request):
    current_year = timezone.now().year
    users = list(User.objects.all())
    roles = set(user.role for user in users)
    role_counts=[User.objects.filter(role=rolein).__len__() for rolein in roles]
    

    plt.figure(figsize=(8, 6))
    plt.pie(role_counts, labels=roles, autopct='%1.1f%%', colors=['blue', 'red', 'green'])
    plt.title('Распределение ролей пользователей')
    plt.savefig("club/static/statistics/stat1.png")

    ages = [current_year - user.date_birth.year for user in users if user.date_birth]
    age_counts = dict(Counter(ages))
    sorted_ages = sorted(age_counts.keys())
    counts = [age_counts[age] for age in sorted_ages]

    plt.figure(figsize=(8, 6))
    plt.bar(sorted_ages, counts, color='yellow', edgecolor='black')
    plt.xlabel('Возраст пользователей')
    plt.ylabel('Количество пользователей')
    plt.title('Распределение возрастов пользователей')
    plt.savefig("club/static/statistics/stat2.png")
    return render(request, "club/statistics.html")