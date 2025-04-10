from django.contrib import admin
from .models import (
    Store,
    Product,
    AcquisitionHistory,
    Watch,
    Art,
    Automobile,
    SalesHistory,
    Bid,
    Wishlist,
    UserExtended

)


# Register your models here.
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(AcquisitionHistory)
admin.site.register(Watch)
admin.site.register(Art)
admin.site.register(Automobile)
admin.site.register(SalesHistory)
admin.site.register(Bid)
admin.site.register(Wishlist)
admin.site.register(UserExtended)
