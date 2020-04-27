#Groups ursl.py file
from django.conf.urls import url
#here we are importing the views
from . import views
app_name = 'groups'

urlpatterns = [
#now when anyone visit your website it is gonna see your list of groups
url(r'^$',views.ListGroups.as_view(),name='all'),
#here we are gonna create our Groups
url(r'^new/$',views.CreateGroup.as_view(),name='create'),
#here the lots of content is because we are slugifing the actuall
url(r'posts/in/(?P<slug>[-\w]+)/$',views.SingleGroup.as_view(),name='single'),
url(r'join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
url(r'leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave')
]
