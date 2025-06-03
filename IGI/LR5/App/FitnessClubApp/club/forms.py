from django import forms
from .models import CommentsModel

class CommentsForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Напишите ваш комментарий...'
            }),
            'rating': forms.Select()
        }
        labels = {
            'text': 'Ваш отзыв',
            'rating': 'Ваша оценка'
        }