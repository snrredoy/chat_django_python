from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    member = models.ManyToManyField(User, blank=True, related_name='member')
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='chat')
    content = models.TextField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)