from django.contrib import admin
from .models import edgar, Roommates, Payments

# Register your models here.

admin.site.register(edgar)
admin.site.register(Roommates)
admin.site.register(Payments)
