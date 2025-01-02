from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Register)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(Checkout)
admin.site.register(Payment)

