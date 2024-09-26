from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    gender = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = CloudinaryField("Image", overwrite=True, format="jpg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    
    def __str__(self):
        return self.username
    

class Post(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField("Image", overwrite=True, format="jpg")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering =["-created_at"]

    
    def __str__(self):
        return self.message
    

class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return self.message
    

class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")


class Follow(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")

    class Meta:
        unique_together = ("followed", "following")