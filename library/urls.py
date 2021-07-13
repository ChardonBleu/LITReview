from django.urls import path

from library import views
from .forms import CustomLoginView

app_name = 'library'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name="register"),
    path('flux/', views.flux, name="flux"),
]
