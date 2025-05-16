from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Chat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='chat')
    content = models.TextField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)