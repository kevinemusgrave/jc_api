from django.test import TestCase
from django.urls import reverse

class APITestCase(TestCase):
    fixtures = ["users", "messages"]

    def test_message_list(self):
        response = self.client.get(reverse("api:list_messages"))
        self.assertEqual(len(response.data), 2)

    def test_add_message(self):
        payload = {
            "text": "Adding a test message",
            "author": 1,
            "parent": ""
        }
        response = self.client.post(reverse("api:add_message"), data=payload)
        response = self.client.get(reverse("api:list_messages"))
        self.assertEqual(len(response.data), 3)

    def test_message_details(self):
        response = self.client.get(
            reverse("api:message_details", kwargs={"message_id": 1})
        )
        self.assertEqual(len(response.data["replies"]), 1)

    def test_add_reply(self):
        payload = {
            "text": "Adding a test message",
            "author": 1,
            "parent": 1
        }
        response = self.client.post(reverse("api:add_message"), data=payload)
        response = self.client.get(
            reverse("api:message_details", kwargs={"message_id": 1})
        )
        self.assertEqual(len(response.data["replies"]), 2)

    def test_list_replies(self):
        response = self.client.get(
            reverse("api:message_replies", kwargs={"message_id": 1})
        )
        self.assertEqual(len(response.data), 1)
        payload = {
            "text": "Adding a test message",
            "author": 1,
            "parent": 1
        }
        response = self.client.post(reverse("api:add_message"), data=payload)
        response = self.client.get(
            reverse("api:message_replies", kwargs={"message_id": 1})
        )
        self.assertEqual(len(response.data), 2)

    def test_bookmark_list(self):
        response = self.client.get(
            reverse("api:list_bookmarks", kwargs={"user_id": 1})
        )
        self.assertEqual(len(response.data), 1)

    def test_add_bookmark(self):
        payload = {
            "message": 1,
            "user": 1
        }
        response = self.client.post(reverse("api:add_bookmark"), data=payload)
        response = self.client.get(
            reverse("api:list_bookmarks", kwargs={"user_id": 1})
        )
        self.assertEqual(len(response.data), 2)

    def test_delete_bookmark(self):
        payload = {
            "message": 2,
            "user": 1
        }
        response = self.client.post(reverse("api:delete_bookmark"), data=payload)
        response = self.client.get(
            reverse("api:list_bookmarks", kwargs={"user_id": 1})
        )
        self.assertEqual(len(response.data), 0)
