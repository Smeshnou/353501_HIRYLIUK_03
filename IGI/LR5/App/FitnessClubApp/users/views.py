from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm
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

    def form_valid(self, form):
        user = self.request.user
        if 'description' in form.changed_data:
            if user.role != 'Instructors' and user.role != 'Instructors':
                form.add_error('description', 'Нет прав на редактирование этого поля')
                return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return self.request.user
    