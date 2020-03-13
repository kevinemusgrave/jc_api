from django.db import models

from jetcake.users.models import User

class Message(models.Model):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, related_name="topics", on_delete=models.PROTECT)
    parent = models.ForeignKey('self', related_name="replies", null=True, blank=True, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    bookmarks = models.ManyToManyField(User, through="Bookmark", related_name="messages")

class Bookmark(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="user_bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_bookmarks")
