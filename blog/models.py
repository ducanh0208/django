from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title
    
def get_absolute_url(self):
    return reverse('post_detail', kwargs={'pk': self.pk})