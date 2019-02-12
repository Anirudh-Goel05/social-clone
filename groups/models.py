from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='No description given yet')
    members = models.ManyToManyField(User,through='GroupMember',related_name='group')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    class Meta:
        unique_together = ['slug']
        # ordering = ['-members']
    def get_absolute_url(self):
        return reverse('group:group_list')

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='member',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group','user',)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    group = models.ForeignKey(Group,related_name='posts',on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True,default='game_of_thrones')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user','text')

    def __str__(self):
        return self.text

class Upvoter(models.Model):
    user = models.ForeignKey(User,related_name='upvoter',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='upvote',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post','user',)

    def __str__(self):
        return self.user.username
