from django.contrib import admin
from .models import Post
from embed_video.admin import AdminVideoMixin
# Register your models here.

class myPostAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Post, myPostAdmin)