from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Review, Ticket, UserFollows


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)
