from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from order.models import Order
from order.permissions import UserIsOwnerOrder
from order.serializers import OrderSerializer

from datetime import datetime, time

class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    start=str(datetime.now())
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerOrder)
    start=OrderListCreateAPIView.start

    error_messages = {
            'error_msg': _('Update or Delete in 15 mins')
    }

    def put(self, request, *args, **kwargs):
        end = str(datetime.now())
        end_ed = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        start_st = datetime.strptime(OrderListCreateAPIView.start, '%Y-%m-%d %H:%M:%S.%f')
        timedelta= end_ed - start_st
        minutes=timedelta.seconds % 3600 / 60.0
        minutes=int(round(minutes))
        if(minutes<150):
            queryset = Order.objects.all()
            return self.update(self, request, *args, **kwargs)
        else:
            raise serializers.ValidationError(self.error_messages['error_msg'])

    def delete(self, request, *args, **kwargs):
        end = str(datetime.now())
        end_ed = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        start_st = datetime.strptime(OrderListCreateAPIView.start, '%Y-%m-%d %H:%M:%S.%f')
        timedelta= end_ed - start_st
        minutes=timedelta.seconds % 3600 / 60.0
        minutes=int(round(minutes))
        if(minutes>15):
            raise serializers.ValidationError(self.error_messages['error_msg'])
