from django.contrib.auth.models import User
from django.db import models

from items.models import Item


class Conversation(models.Model):
    # Item is referenced here, so that when an item is deleted, the mesages are deleted also
    item = models.ForeignKey(
        Item, related_name='conversations', on_delete=models.CASCADE)
    # Conversation between many users on one item and many users on many items
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='created_messages', on_delete=models.CASCADE)
