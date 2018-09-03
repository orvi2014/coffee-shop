from django.contrib import admin
from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "cup_count", "lat", "long", "date_created")
    list_filter = ("date_created",)


admin.site.register(Order, OrderAdmin)
