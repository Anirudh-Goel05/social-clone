from django.forms import ModelForm
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email','password',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    def clean_password_conf(self):
        confirm_password = self.cleaned_data['password_conf']
        password = self.cleaned_data['password']
        if confirm_password != password:
            raise forms.ValidationError("Passwords do not match")

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
