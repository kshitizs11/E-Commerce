from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views import generic
# Create your views here.
from django.shortcuts import get_object_or_404
#we are installing the models here
from groups.models import Group,GroupMember
from django.db import IntegrityError
from . import models
from flask import request
#now this is view whena user log into the site now want to create his own group than this is the view for that
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    #now this is the view in which where we are connect it with the user
    #further we need to create it to our templates
    model = Group

#now this is the part where your all info related to the groups like your posts get stored
class SingleGroup(generic.DetailView):
    model = Group

#here is all the grps are shown as the lists
class ListGroups(generic.ListView):
    model =  Group
#redirect is a djangoview that is going to redirect the user once it is login
class JoinGroup(LoginRequiredMixin,generic.RedirectView):
#it is going to redirect to the page whereever you want them to redirect to and grab that url
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
#that is actually the check that whether this person is already the member of the group
    def get(self,*args,**kwargs):
        #this is going to tellyou that return this person the group that this person is lookingat or return 404 page
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            #this is going to get the group member and the current user and group
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a Member!')
        else:
            messages.success(self.request,'You Are Now A Member!')
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    #redirect to the page once they leave the page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
#fro not leave the group if they are not part of that group
    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(
            user = self.request.user,
            group__slug = self.kwargs.get('slug')
            ).get()
        except  models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this Group!')
        else:
            membership.delete()
            messages.success(self.request,'You Have Left The Group!')
        return super().get(request,*args,**kwargs)
