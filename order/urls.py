from django.conf.urls import url
from order.views import OrderListCreateAPIView, OrderDetailAPIView

urlpatterns = [
    url(r'^$', OrderListCreateAPIView.as_view(), name="list"),
    url(r'^(?P<pk>[0-9]+)/$', OrderDetailAPIView.as_view(), name="detail"),
]
