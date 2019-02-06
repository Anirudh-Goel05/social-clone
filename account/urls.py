from django.urls import path,include
from .views import SignUpView,HomePageView,SignInView,sign_out_view,UserPostListView,UserProfileView,UserListView,user_self_profile

app_name = 'account'
urlpatterns = [
    path('sign_up/',SignUpView.as_view(),name='sign_up'),
    path('',HomePageView.as_view(),name='home_page'),
    path('sign_in/',SignInView.as_view(),name='sign_in'),
    path('sign_out/',sign_out_view,name='sign_out'),
    path('user/',UserPostListView.as_view(),name='user_posts'),
    path('user/<int:pk>/',UserProfileView.as_view(),name='user_profile'),
    path('users_all/',UserListView.as_view(),name='user_list'),
    path('user/self/',user_self_profile,name='user_self_profile'),
]
