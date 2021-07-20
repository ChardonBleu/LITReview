from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include

from library import views
from LITReview import settings


app_name = 'library'

urlpatterns = [
    path('flow/', views.flow, name="flow"),
    path('', include('account.urls', namespace='account'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
