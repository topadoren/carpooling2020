from django.contrib import admin
from .models import AppUser
from .models import Vehicle
from .models import Trip
from .models import Qualification

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Vehicle)
admin.site.register(Trip)
admin.site.register(Qualification)