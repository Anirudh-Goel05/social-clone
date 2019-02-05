from django.db import models
from groups.models import Group
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    group = models.ForeignKey(Group,related_name='posts',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user','text')
