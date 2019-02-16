from django.urls import path,include
from . views import (CreateGroupView,GroupListView,GroupDetailView,add_group_member,
                    remove_group_member,PostListView,PostCreateView,
                    upvote,downvote,)
app_name = 'group'

urlpatterns = [
    path('create_group/',CreateGroupView.as_view(),name='create_group'),
    path('',GroupListView.as_view(),name='group_list'),
    path('<slug:slug>/',GroupDetailView.as_view(),name='group_detail'),
    path('<slug:slug>/join/',add_group_member,name='join_group'),
    path('<slug:slug>/leave/',remove_group_member,name='leave_group'),
    path('<slug:slug>/posts/',PostListView.as_view(),name='posts_list'),
    path('<slug:slug>/post_create/',PostCreateView.as_view(),name='posts_create'),
    path('<slug:slug>/<int:pk>/upvote/',upvote,name='posts_upvote'),
    path('<slug:slug>/<int:pk>/downvote/',downvote,name='posts_downvote'),
]
