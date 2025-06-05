from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm
from club.models import ScheduleModel
from calendar import LocaleHTMLCalendar
from django.utils import timezone
# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    success_url = reverse_lazy('user_profile')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        participated_schedule = ScheduleModel.objects.filter(users=user).order_by('start_time')
        
        if user.role == 'Instructors':
            instructed_schedule = ScheduleModel.objects.filter(instructor=user).order_by('start_time')
            context['instructed_schedules'] = instructed_schedule
        
        context['participated_schedules'] = participated_schedule

        cal = LocaleHTMLCalendar(locale='ru_RU')
        today = timezone.now()
        html_calendar = cal.formatmonth(today.year, today.month)
        context['calendar'] = html_calendar
        return context

    def form_valid(self, form):
        user = self.request.user
        if 'description' in form.changed_data:
            if user.role != 'Instructors' and user.role != 'Instructors':
                form.add_error('description', 'Нет прав на редактирование этого поля')
                return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return self.request.user
    