from django.urls import path
from . import views
import posts.views as posts_views



urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:id>/', posts_views.get_post, name='get_post'),
    path('post/new/', posts_views.submit_new_post, name='submit_new_post'),
    path('profile/logout', views.profile_logout, name='profile_logout'),
]