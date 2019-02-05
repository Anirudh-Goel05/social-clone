from django.forms import ModelForm
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_conf = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email','password',)
        
    def clean_password_conf(self):
        password_conf = self.cleaned_data['password_conf']
        password = self.cleaned_data['password']
        if password_conf != password:
            raise forms.ValidationError("Passwords do not match")

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
