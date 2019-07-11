from django.urls import path

from . import views

urlpatterns = [
    path('room/<str:room_name>', views.room, name='room'),
    path('validate-room', views.validate_room_name, name='validate-room'),
    path('get-rooms', views.get_rooms, name='get_rooms'),
    path('', views.index, name='index'),
]
