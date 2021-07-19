from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    """
    customization of the UserAdmin class in order to make it call a
    personalized form for the creation of a new user
    """
    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)
