from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    subject = models.CharField(max_length=200)
    is_readed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('creation_date',)
