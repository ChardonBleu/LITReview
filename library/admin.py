from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Review, Ticket, UserFollows
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm


admin.site.register(User, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)
