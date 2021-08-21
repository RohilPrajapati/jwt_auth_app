from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE

class Author(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=False,blank=False)
    password = models.CharField(max_length=270,null=False,blank=False)
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    posted_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
