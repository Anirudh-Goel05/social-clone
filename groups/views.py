from django.shortcuts import render
from .models import Group,GroupMember
from django.views.generic.edit import CreateView,FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
User = get_user_model()

class CreateGroupView(CreateView):
    template_name = 'groups/create_group.html'
    model = Group
    fields = ['name','description',]

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        GroupMember.objects.create(group=self.object,user=self.request.user)
        return HttpResponseRedirect(reverse('group:group_detail',kwargs={'slug':self.object.slug}))


class GroupListView(ListView):
    template_name = 'groups/group_list.html'
    model = Group
    paginate_by = 10
    context_object_name = 'groups'

class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_group = get_object_or_404(Group, slug=self.kwargs['slug'])
        context['member_count'] =  cur_group.member.count() #Get count of group members
        return context

@login_required
def add_group_member(request,slug):
    if request.method == 'POST':
        group = get_object_or_404(Group, slug=slug)
        user_already_in_group = GroupMember.objects.filter(user=request.user,group=group)
        if user_already_in_group:
            return HttpResponse('You are already in this group')
        GroupMember.objects.create(group=group,user=request.user)
        return HttpResponseRedirect(reverse('group:group_detail',kwargs={'slug':slug}))
    else:
        return render(request,'groups/join_group_form.html',context={'slug':slug})

@login_required
def remove_group_member(request,slug):
    if request.method == 'POST':
        group = get_object_or_404(Group, slug=slug)
        user_already_in_group = GroupMember.objects.filter(user=request.user,group=group)
        if user_already_in_group:
            user_already_in_group.delete()
            return HttpResponseRedirect(reverse('group:group_detail',kwargs={'slug':slug}))
        return HttpResponse('You are not in this group')
    else:
        return render(request,'groups/leave_group_form.html',context={'slug':slug})
