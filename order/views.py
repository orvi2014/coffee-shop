from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator

from order.models import Order
from order.permissions import UserIsOwnerOrder
from order.serializers import OrderSerializer

from datetime import datetime, time
from django.core.mail import send_mail

# Order List Create

class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (UserIsOwnerOrder, )
    start=str(datetime.now())

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Order Detail API

class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = []
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (UserIsOwnerOrder, )
    minutes_str="0"
    minutes=0
    # Get method
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    # update method
    def put(self, request, *args, **kwargs):
        # custom default_error_messages
        default_error_messages = {
            'error_messages': _('Update or delete within 15 minutes')
        }
        # Can not update after 15 minutes_str
        # Don't reload
        # It's open a new session everytime. Just wait here 15 mins it would
        # url need to change in future
        end = str(datetime.now())
        end_ed = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        start_st = datetime.strptime(OrderListCreateAPIView.start, '%Y-%m-%d %H:%M:%S.%f')
        timedelta= end_ed - start_st
        minutes_str=timedelta.seconds % 3600 / 60.0
        minutes=int(round(minutes_str))

        if minutes<15:
            #send_mail("Update Order", "Your Order has been Updated", "orvidas12@gmail.com", **kwargs)
            return self.update(request, *args, **kwargs)
        #else:
        #    raise serializers.ValidationError(self.error_messages['error_messages'])

    def delete(self, request, *args, **kwargs):
        if (self.minutes<15):
            return self.destroy(request, *args, **kwargs)
