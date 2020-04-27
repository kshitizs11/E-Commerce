from django.conf.urls import url

from . import views
app_name = 'posts'

urlpatterns = [
url(r'^$',views.PostList.as_view(),name='all'),
#fro the post that user has created
url(r'new/$',views.CreatePost.as_view(),name='create'),
#for the users post
url(r'by/(?P<username>[-\w]+)',views.UserPosts.as_view(),name='for_user'),
#it is for showing all posts of users and the below mentioned is the primay key
url(r'by/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='single'),
url(r'delete/(?P<pk>\d+)/$',views.DeletePost.as_view(),name='delete')
]
