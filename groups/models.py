from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
#import misaka
#for getting your current use model
from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
#comes to this later
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    #it helps in urls and on the other hand unique make sure the two names do not overlap
    slug = models.SlugField(allow_unicode=True,unique=True)
    description =  models.TextField(blank=True,default="")
    #here if it want to use the html text
    description_html = models.TextField(editable=False,default="",blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        #here groups:single is gonna work when ur link get set
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    #this is gona link to Group by memberships key
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    #this is gonna take user_groups as key and it is gonna connect it with the User model that is installed by using library
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    #talk about this later
    class Meta:
        unique_together = ('group','user')
