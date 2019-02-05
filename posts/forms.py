from django.forms import ModelForm
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text')
