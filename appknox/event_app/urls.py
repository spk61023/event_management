from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    #admin api's -- TODO create routes with api/v1/
    path('', ListCreateEventAPIView.as_view(), name='get_post_events'),
    path('<uuid:pk>/', RetrieveUpdateDestroyEventAPIView.as_view(), name='get_delete_update_event'),
    path('theatres/', ListCreateTheatreAPIView.as_view(), name='get_post_events'),
    path('theatres/<uuid:pk>/', RetrieveUpdateDestroyTheatreAPIView.as_view(), name='get_delete_update_event'),

    #user api's
    path('all-events/', UserViewAllEvents.as_view(), name='user_view_all_events'),
    path('register-event/', UserBookEventTicket.as_view(), name='user_register_event'),
    path('view-ticket/', UserViewTicket.as_view(), name='user_view_ticket'),
    path('all-registered/', UserViewAllRegisteredEvents.as_view(), name='user_view_all_registered'),
]
