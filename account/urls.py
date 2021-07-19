from django.urls import path
from django.contrib.auth import views as auth_views


from account import views
from .views import CustomLoginView


app_name = 'account'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
]
