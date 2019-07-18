from django.urls import path

from . import views

urlpatterns = [
    path('room/<str:room_name>', views.room, name='room'),
    path('get-students', views.refresh_student_list, name='get_students'),
    path('validate-room', views.validate_room_name, name='validate-room'),
    path('get-rooms', views.get_rooms, name='get_rooms'),
    path('pause-module', views.pause_module, name='pause'),
    path('', views.index, name='index'),
]
