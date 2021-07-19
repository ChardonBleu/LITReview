from django.urls import path
from django.conf.urls.static import static

from library import views
from LITReview import settings


app_name = 'library'

urlpatterns = [
    path('', views.flow, name="flow"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
