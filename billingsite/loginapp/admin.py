from django.contrib import admin
from .models import homeMOTD, Roommates, Payments

# Register your models here.

admin.site.register(homeMOTD)
admin.site.register(Roommates)
admin.site.register(Payments)
