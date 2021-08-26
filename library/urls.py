from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include

from library import views
from library.views import FollowingView, SubscriptionDeletionView
from LITReview import settings


app_name = 'library'

urlpatterns = [
    path('flow/', views.flow, name="flow"),
    path('', include('account.urls', namespace='account')),
    path('ticket/', views.ticket_creation, name="ticket_creation"),
    path('review/', views.review_creation, name="review_creation"),
    path('review_ticket/<int:ticket_id>/',
         views.review_for_ticket, name="review_ticket"),

    path('posts/', views.posts, name="posts"),
    path('ticket/<int:ticket_id>/modify/',
         views.post_modification_ticket, name="modify_ticket"),
    path('ticket/<int:ticket_id>/delete/',
         views.ticket_deletion, name="delete_ticket"),
    path('review/<int:review_id>/modify/',
         views.post_modification_review, name="modify_review"),
    path('review/<int:review_id>/delete/',
         views.review_deletion, name="delete_review"),

    path('following/', FollowingView.as_view(), name="following"),
    path('following/<int:userfollows_id>/delete/',
         SubscriptionDeletionView.as_view(), name="delete_subscription")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
