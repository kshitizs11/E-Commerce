from django.db import models
from django.urls import reverse
from django.conf import settings

#import misaka

from groups.models import Group

# Create your models here.
from django.contrib.auth import get_user_model
#that is just gonna connect you to the to the current user
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    #it is gonna connect you with the group
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        #self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        #we are using primary key as a link to post back to the url
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        #- at created represent the latest
        ordering = ['-created_at']
        #this is gonna uniquely connect every user with its message
        unique_together = ['user','message']
