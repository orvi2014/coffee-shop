from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.permissions import UserIsOwnerOrder
from order.serializers import OrderSerializer

import datetime

start=0
class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        start=datetime.now()
        serializer.save(user=self.request.user)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = []
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerOrder)
