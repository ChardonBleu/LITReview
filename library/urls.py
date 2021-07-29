from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include

from library import views
from LITReview import settings


app_name = 'library'

urlpatterns = [
    path('flow/', views.flow, name="flow"),
    path('', include('account.urls', namespace='account')),
    path('ticket/', views.ticket_creation, name="ticket_creation"),
    path('review/', views.review_creation, name="review_creation"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
