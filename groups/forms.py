from django.forms import ModelForm
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User


class JoinGroupForm(forms.Form):
    
