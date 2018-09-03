import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from order.models import Order
from order.serializers import OrderSerializer


class OrderListCreateAPIViewTestCase(APITestCase):
    url = reverse("order:orderadd")
    #create a new user
    def setUp(self):
        self.username = "orvi"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    # check api authentication
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    # create order
    def test_create_order(self):
        response = self.client.post(self.url, {"cup_count": "10","lat":"92.83","long":"92"})
        self.assertEqual(201, response.status_code)

    def test_user_orders(self):
        """
        Test to verify user orders list
        """
        Order.objects.create(user=self.user, cup_count="10",lat="92.83",long="92")
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == Order.objects.count())


class OrderDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.order = Order.objects.create(user=self.user,cup_count="10",lat="92.83",long="92")
        self.url = reverse("order:detail", kwargs={"pk": self.order.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_order_object_bundle(self):
        """
        Test to verify order object bundle
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        order_serializer_data = OrderSerializer(instance=self.order).data
        response_data = json.loads(response.content)
        self.assertEqual(order_serializer_data, response_data)

    def test_order_object_update_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        response = self.client.put(self.url, {"cup_count": "hacked","lat":"92.83","long":"92"})
        self.assertEqual(403, response.status_code)

        # HTTP PATCH
        response = self.client.patch(self.url, {"cup_count": "hacked","lat":"92.83","long":"92"})
        self.assertEqual(403, response.status_code)

    def test_order_object_update(self):
        response = self.client.put(self.url, {"cup_count": "50","lat":"102.83","long":"102"})
        response_data = json.loads(response.content)
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(response_data.get("cup_count"), order.cup_count)
        self.assertEqual(response_data.get("lat"), order.lat)
        self.assertEqual(response_data.get("long"), order.long)

    def test_order_object_delete_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_order_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
