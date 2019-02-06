from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,FormView
from .models import Profile
from .forms import UserProfileForm,UserLoginForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from groups.models import Group,GroupMember,Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'account/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context

class SignUpView(FormView):
    template_name = 'account/profile_create_form.html'
    form_class = UserProfileForm


    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        user_profile = Profile(user=user)
        return HttpResponseRedirect(reverse('account:sign_in'))

class SignInView(FormView):
    template_name='account/sign_in_form.html'
    form_class = UserLoginForm
    success_url = '/'

    def form_valid(self,form):
        username = form['username'].value()
        password = form['password'].value()
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request,user)
            # valuenext= self.request.POST.get('next')
            valuenext= self.request.GET.get('next')
            if valuenext:
                return HttpResponseRedirect(valuenext)
            return HttpResponseRedirect(reverse('home_page'))
        else:
            messages.error(self.request,'username or password not correct')
            return HttpResponseRedirect(reverse('account:sign_in'))
        return super().form_valid(form)

@login_required
def sign_out_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

class UserPostListView(LoginRequiredMixin,ListView):
    template_name = 'account/post_list.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        groups = GroupMember.objects.filter(user=user).values('group')
        posts = Post.objects.filter(group=0)
        for group in groups:
            group_id = group['group']
            post = Post.objects.filter(group=group_id).order_by('-created_at').values()
            posts = posts|post
        posts = posts.order_by('-created_at')
        return posts

class UserProfileView(LoginRequiredMixin,ListView):
    template_name = 'account/user_profile.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = get_object_or_404(User,id=pk)
        return Post.objects.filter(user=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = get_object_or_404(User,id=pk)
        total_posts = Post.objects.filter(user=user).count()
        context['user'] = user
        context['total_posts'] = total_posts
        return context

class UserListView(ListView):
    template_name = 'account/user_list.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all().order_by('username')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        total_users = User.objects.count()
        context['total_users'] = total_users
        return context

@login_required
def user_self_profile(request):
    user = request.user
    return HttpResponseRedirect(reverse('account:user_profile',kwargs={'pk':user.id}))
