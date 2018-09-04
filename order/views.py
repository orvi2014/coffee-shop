from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from order.models import Order
from order.permissions import UserIsOwnerOrder, IsAdminUser
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
    permission_classes = (UserIsOwnerOrder, )
    error_messages = {
            'error_msg': _('Update or Delete in 15 mins')
    }
    def get_queryset(self):
        group = self.kwargs["id"]
        return Order.objects.get(group = group)

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
    def get(self, request, pk, *args, **kwargs):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self,request):
        end = str(datetime.now())
        end_ed = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        start_st = datetime.strptime(OrderListCreateAPIView.start, '%Y-%m-%d %H:%M:%S.%f')
        timedelta= end_ed - start_st
        minutes=timedelta.seconds % 3600 / 60.0
        minutes=int(round(minutes))
        if(minutes>1):
            order = request.data.get('cup_count', None)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(True)
            else:
                raise serializers.ValidationError(self.error_messages['error_msg'])
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
