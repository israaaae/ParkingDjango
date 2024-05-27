from django.contrib import admin
from .models import Vehicle
from .models import ParkingExit
from .models import ParkingEntry
from django.contrib import admin

admin.site.register(Vehicle)
admin.site.register(ParkingEntry)
admin.site.register(ParkingExit)

