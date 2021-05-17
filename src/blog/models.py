from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def get_absolute_url(self):
        return reverse('post_detail',args=[str(self.id)])

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()


    def __str__(self):
        return f"Comment  by {self.name} on {self.post}"


