from django.contrib import admin

# Register your models here.
from user.models import CustomUser

admin.site.register(CustomUser)