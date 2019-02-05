from django.shortcuts import render
from .models import Post
from groups.models import Group,GroupMembers
from django.views.generic.edit import CreateView,FormView
from django.views.generic.list import ListView
from django.urls import reverse
# Create your views here.
class PostCreateView(FormView):
    template_name = 'groups/post_create_form.html'
    form_class = PostCreateForm

    def form_valid(self,form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return reverse('posts:posts-list',slug=self.request.slug)
        
class PostListView(ListView):
    template_name = 'groups/post_list.html'
    model = Post
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset():
        pass
