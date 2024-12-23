from django.urls import path
from . import views
import posts.views as posts_views
import profiles.views as profiles_views
import comments.views as comments_views

urlpatterns = [
    ## Frontend  Templates ##

    path('', views.home, name='home'),
    path('bookmarked/', views.bookmarked, name='bookmarked'),

    # Comments
    path('seed/comment/', comments_views.post_comment, name='seed_comment'),

    # Interactables
    path('love/<str:type>/<int:id>/', views.love_content, name='love_content'),
    path('bookmark/<str:type>/<int:id>/', views.bookmark_content, name='bookmark_content'),

    ### Profiles ###
    path('profile/logout', profiles_views.profile_logout, name='profile_logout'),
    path('profile/signup/', profiles_views.request_signup, name='profile_signup'),
    path('profile/login/', profiles_views.request_login, name='profile_login'),
    path('profile/account_reset/', profiles_views.request_account_reset, name='request_account_reset'),

    ### Posts ###
    path('post/<int:id>/', posts_views.get_post, name='get_post'),
    path('post/new/', posts_views.submit_new_post, name='submit_new_post'),
]