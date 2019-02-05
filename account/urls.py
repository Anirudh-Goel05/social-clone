from django.urls import path,include
from .views import SignUpView,HomePageView,SignInView,sign_out_view

app_name = 'account'
urlpatterns = [
    path('sign_up/',SignUpView.as_view(),name='sign_up'),
    path('',HomePageView.as_view(),name='home_page'),
    path('sign_in/',SignInView.as_view(),name='sign_in'),
    path('sign_out/',sign_out_view,name='sign_out'),
]
