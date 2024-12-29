from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.forms import CustomUserProfileForm
from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = CustomUserProfileForm.Meta.fields


admin.site.register(CustomUser, CustomUserAdmin)
