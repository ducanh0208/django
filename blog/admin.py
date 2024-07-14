from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'date']
admin.site.register(Post, PostAdmin)
