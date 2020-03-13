from rest_framework import serializers

from .models import Message, Bookmark

class MessageSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField("get_reply_count")

    def get_reply_count(self, obj):
        return obj.replies.all().count()

    class Meta:
        model = Message
        fields = ["text", "author", "parent", "date_posted", "reply_count"]

class DetailSerializer(serializers.ModelSerializer):
    replies = MessageSerializer(many=True)
    reply_count = serializers.SerializerMethodField("get_reply_count")

    def get_reply_count(self, obj):
        return obj.replies.all().count()

    class Meta:
        model = Message
        fields = ["text", "author", "parent", "date_posted", "replies", "reply_count"]


class BookmarkSerializer(serializers.ModelSerializer):
    message = MessageSerializer()
    class Meta:
        model = Bookmark
        fields = ["message"]
