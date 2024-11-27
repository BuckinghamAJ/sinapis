from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:id>/', views.get_post, name='get_post'),
    path('post/new/', views.submit_new_post, name='submit_new_post'),
]