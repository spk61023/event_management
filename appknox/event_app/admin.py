from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Theatre)
admin.site.register(Show)
admin.site.register(Seat)
admin.site.register(BookedSeat)
