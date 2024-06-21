from django.db import models
from django.conf import settings

# Create your models here.

class UserMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_receiver')
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_message'

    def __str__(self):
        return f"{self.text} | {self.sender} - {self.receiver}"

    def user_auth(self, user):
        return self.sender == user

    def edit_message(self, text):
        self.text = text
        self.save()



