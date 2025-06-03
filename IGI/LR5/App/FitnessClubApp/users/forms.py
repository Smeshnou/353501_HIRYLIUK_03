import datetime
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import User



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+375 XX XXX-XX-XX'}), region='BY', label="Телефон (Беларусь)")
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=(range(this_year- 100, this_year+1))), initial=datetime.date.today())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES[:-1], initial='Clients', label='Выберите роль', widget=forms.Select)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email','date_birth','first_name','last_name', 'phone_number', 'role', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_birth': 'Дата Рождения',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'date_birth': forms.DateTimeInput(attrs={'class': 'form-input'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
    
    def clean_date_birth(self):
        date_birth = self.cleaned_data['date_birth']
        today = datetime.date.today()
        age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
        
        if age < 18:
            raise forms.ValidationError("Регистрация доступна только для лиц старше 18 лет!")
        
        return date_birth
    
    def save(self, commit = ...):
        user = super().save(commit)
        user.groups.add(Group.objects.get(name=self.cleaned_data['role']))
        #if(Group.objects.get(name=self.cleaned_data['role']) == 'Instructors'):
           # user.user_permissions.add(29)
        return user
    
    
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Имя пользователя',widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail',widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = PhoneNumberField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+375 XX XXX-XX-XX'}), region='BY', required=False, label="Телефон (Беларусь)")
    this_year = datetime.date.today().year
    date_birth = forms.DateField(disabled=True, label='Дата Рождения', widget=forms.SelectDateWidget(years=(range(this_year- 100, this_year+1))))
    role = forms.ChoiceField(disabled=True, choices=User.ROLE_CHOICES, label='Роль', widget=forms.Select)

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'date_birth', 'description']
        labels = {
            'photo': 'Фотография',
            'first_name': 'Имя', 
            'last_name': 'Фамилия',
            'date_birth': 'Дата Рождения',
        }
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}), 
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'date_birth': forms.DateTimeInput(attrs={'class': 'form-input'}),
        }

    def clean_date_birth(self):
        date_birth = self.cleaned_data['date_birth']
        today = datetime.date.today()
        age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
        
        if age < 18:
            raise forms.ValidationError("Регистрация доступна только для лиц старше 18 лет!")
        
        return date_birth
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.role != 'Admins' and self.instance.role != 'Instructors':
            self.fields['description'].widget.attrs['disabled'] = True
            self.fields['description'].help_text = 'Доступно только для инструкторов и администраторов'