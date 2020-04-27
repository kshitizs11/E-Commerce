from django.shortcuts import render
#this is the place for views of our posts
#we have imported it here to provide user the facility that when it log in it can see options to see its groups postd
from django.contrib.auth.mixins import LoginRequiredMixin
#it is the one which is gonna provide you the ability to delete the post
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib import messages
from braces.views import SelectRelatedMixin


from . import models
from . import forms

#this is the which is gonna use when a user login
#than it is the one that is going to provide all the functionality to it
from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    #connection to the model post
    model = models.Post
    #the user and the group that the post belongs to and it is also going to act as the forign key
    select_related = ('user','group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            #here User is the ORM object relational model that django provide
            #username is (iexact) exactly equal to the whoever logged in
            #also use to fetch the post of the user
            #this is all for the current user in which it is going to highlight the name of the current user
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
#here we are returning the context data object of the user
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


#here we are getting the query set for the post and than we are gonna filter the users user template_name
class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    #here we are connecting the message and the posts of the user
    fields = ('message','group')
    model = models.Post
#all this is to connect the actuall post to user itself
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)



class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    #it is going to take you to all the post once you delete the post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)


    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
