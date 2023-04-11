from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending','pending'),
        ('Archived','archived'),
        ('Sucsess','sucsess')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tasks")
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES,default='pending',max_length=8)