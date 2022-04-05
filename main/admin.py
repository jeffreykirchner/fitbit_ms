from django.contrib import admin

from main.models import Parameters
from main.models import RegistrationRequest
from main.models import FitBitUser

# Register your models here.

admin.site.register(Parameters)
admin.site.register(RegistrationRequest)
admin.site.register(FitBitUser)
