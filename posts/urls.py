from django.urls import path,include
from . import views

app_name = 'posts'

urlpatterns = [
    path('<slug:slug>/',PostListView.as_view(),name='posts-list'),
    path('<slug:slug>/create_post',PostCreateView.as_view(),name='post-create'),
]
