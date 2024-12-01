from django.db import models

# Create your models here.
class Comment(models.Model):
    author = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True) 
    text = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.name or 'Anonymous'} on {self.created_at}"