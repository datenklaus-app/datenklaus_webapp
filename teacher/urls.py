from django.urls import path

from . import views

urlpatterns = [
    #  path('room/<str:room_name>', views.room, name='room'),
    path('join-room', views.join, name='teacher_join'),
    path('leave', views.leave_room, name='teacher_leave'),
    path('students', views.students, name='students'),
    path('validate-room', views.validate_room_name, name='validate-room'),
    path('rooms', views.rooms, name='rooms'),
    path('results/<str:room_name>', views.results, name='results'),
    path('control', views.control_cmd, name='pause'),
    path('test-students', views.create_test_students, name='test-students'),
    path('', views.index, name='teacher_index'),
]
