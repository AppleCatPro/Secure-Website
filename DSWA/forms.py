from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class DataForm(forms.ModelForm):
    class Meta:
        model = ConfidentialData
        fields = ['title', 'description', 'is_encrypted']
        labels = {
            'title': 'Confidential Data title',
            'description': 'Confidential Data description',
            'is_encrypted': 'Is Encrypted'
        }

    def clean_data(self):
        data = self.cleaned_data['data']
        # Дополнительные проверки или обработка данных
        return data


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'date_of_birth', 'gender', 'is_verified')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'date_of_birth', 'gender', 'is_verified')


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'date_of_birth', 'gender', 'is_verified')
