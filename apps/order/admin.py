from django.contrib import admin
from .models import (
    MoviePurchases,
    OrderItems
)


admin.site.register(MoviePurchases)
admin.site.register(OrderItems)
