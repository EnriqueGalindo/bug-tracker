from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from custom_user.models import MyCustomUser


# Register your models here.
admin.site.register(MyCustomUser, UserAdmin)