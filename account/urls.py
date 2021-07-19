from django.urls import path
from django.contrib.auth import views as auth_views

from ..library import views as library_views

from account import views
from .views import CustomLoginView


app_name = 'library'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('flow/', library_views.flow, name='flow'),
]
