from django.contrib import admin
from . import models

# Register your models here.
#This is a class that is used to register models
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember
    
admin.site.register(models.Group)
