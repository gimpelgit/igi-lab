from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Car)
admin.site.register(Payment)
admin.site.register(ParkingSpace)
admin.site.register(Accrual)
admin.site.register(Coupon)
admin.site.register(CouponClient)
admin.site.register(BankCard)