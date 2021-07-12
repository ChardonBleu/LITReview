from django.urls import path

from library import views

app_name = 'library'

urlpatterns = [
    path('', views.log_in, name="log_in"),
    path('register/', views.register, name="register")

]
