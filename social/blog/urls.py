from django.urls import path
from .import views
from django.conf.urls import url
from blog.feeds import LatestPostsFeed
app_name = 'blog'

urlpatterns = [
# post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('contact/',views.contact, name='contact'),
    path('<int:pk>/view/', views.post_detail, name='post_detail'),
    path('<int:pk>/share/', views.share, name='share'),
    path('create/', views.create_post, name ='create_post'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    url(r'^category$', views.show_category, name='category'),
    path('post_random/',views.post_random, name='posts'),
    path('newsletter/', views.news, name= 'new'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),
]