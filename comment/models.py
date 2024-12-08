from django.db import models
from django.contrib import admin

# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True) 
    text = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f"Comment by {self.name or 'Anonymous'} on {self.created_at}"
    
admin.site.register(Comment)