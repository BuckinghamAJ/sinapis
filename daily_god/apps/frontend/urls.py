from django.urls import path
from . import views
import posts.views as posts_views
import profiles.views as profiles_views
import comments.views as comments_views
import prayers.views as prayers_views
import quotes.views as quotes_views

urlpatterns = [
    ## Frontend  Templates ##

    path('', views.home, name='home'),
    path('bookmarked/', views.bookmarked, name='bookmarked'),

    # Comments
    path('seed/comment/', comments_views.post_comment, name='seed_comment'),
    path('seed/comment/upvote/<int:id>/', comments_views.upvote, name='upvote_comment'),
    path('seed/comment/downvote/<int:id>/', comments_views.downvote, name='downvote_comment'),

    # Interactables
    path('love/<str:type>/<int:id>/', views.love_content, name='love_content'),
    path('bookmark/<str:type>/<int:id>/', views.bookmark_content, name='bookmark_content'),

    ### Profiles ###
    path('profile/logout', profiles_views.profile_logout, name='profile_logout'),
    path('profile/signup/', profiles_views.request_signup, name='profile_signup'),
    path('profile/login/', profiles_views.request_login, name='profile_login'),
    path('profile/account_reset/', profiles_views.request_account_reset, name='request_account_reset'),
    path('profile/', profiles_views.get_profile, name='get_profile'),
    path('profile/update/', profiles_views.update_profile, name='update_profile'),
    path('profile/pic/', profiles_views.get_profile_pic, name='get_profile_pic'),


    ### Posts ###
    path('post/<int:id>/', posts_views.get_post, name='get_post'),
    path('post/new/', posts_views.submit_new_post, name='submit_new_post'),
    path('post/form/blank', posts_views.blank_form, name='new_blank_form'),


    ### Prayers ###
    path('prayer/<int:id>/', prayers_views.get_prayer, name='get_prayer'),
    path('prayer/new/', prayers_views.submit_new_prayer, name='submit_new_prayer'),

    ### Quotes ###
    path('quote/<int:id>/', quotes_views.get_quote, name='get_quote'),
    path('quote/new/', quotes_views.submit_new_quote, name='submit_new_quote'),
]
