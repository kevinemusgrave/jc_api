from django.urls import path

from .views import (
    ListMessages,
    AddMessage,
    MessageDetails,
    ViewBookmarks,
    AddBookmark,
    DeleteBookmark
)

app_name = "api"
urlpatterns = [
    path("message/", view=ListMessages.as_view(), name="list_messages"),
    path("message/add/", view=AddMessage.as_view(), name="add_message"),
    path("message/<int:message_id>/", view=MessageDetails.as_view(), name="message_details"),
    path("message/<int:message_id>/replies/", view=ListMessages.as_view(), name="message_replies"),

    path("bookmarks/<int:user_id>/", view=ViewBookmarks.as_view(), name="list_bookmarks"),
    path("bookmarks/add/", view=AddBookmark.as_view(), name="add_bookmark"),
    path("bookmarks/delete/", view=DeleteBookmark.as_view(), name="delete_bookmark"),
]
