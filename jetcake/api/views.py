from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Message, Bookmark
from .serializers import MessageSerializer, DetailSerializer, BookmarkSerializer

class ListMessages(APIView):
    def get(self, request, *args, **kwargs):
        if kwargs.get("message_id", None) is not None:
            #print("message")
            messages = Message.objects.filter(parent=kwargs.get("message_id", None))
        else:
            messages = Message.objects.filter(parent__isnull=True)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class AddMessage(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetails(APIView):
    def get(self, request, *args, **kwargs):
        message = Message.objects.get(id=kwargs.get("message_id"))

        serializer = DetailSerializer(message)
        return Response(serializer.data)


class ViewBookmarks(APIView):
    def get(self, request, *args, **kwargs):
        bookmarks = Bookmark.objects.filter(user_id=kwargs.get("user_id"))
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)


class AddBookmark(APIView):
    def post(self, request, *args, **kwargs):
        exists = Bookmark.objects.filter(
            message_id=request.data["message"],
            user_id=request.data["user"]
        ).count()
        if exists > 0:
            return Response({"success": False, "error": "Bookmark already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                bookmark = Bookmark.objects.create(
                    message_id=request.data["message"],
                    user_id=request.data["user"]
                )
            except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": True})


class DeleteBookmark(APIView):
    def post(self, request, *args, **kwargs):
        try:
            bookmark = Bookmark.objects.filter(
                message_id=request.data["message"],
                user_id=request.data["user"]
            ).delete()
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": True})
