from django.urls import path
from django.contrib.auth import views as auth_views

from library import views
from .views import CustomLoginView

app_name = 'library'

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('flux/', views.flux, name="flux"),
]
