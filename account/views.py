from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,FormView
from .models import Profile
from .forms import UserProfileForm,UserLoginForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


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

def sign_out_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))
