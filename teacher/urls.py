from django.urls import path

from . import views

urlpatterns = [
    #  path('room/<str:room_name>', views.room, name='room'),
    path('create-room', views.create_room, name='teacher_create_room'),
    path('students', views.get_students, name='students'),
    path('validate-room', views.validate_room_name, name='validate_room'),
    path('rooms', views.get_rooms, name='rooms'),
    path('results/<str:room_name>', views.results, name='results'),
    path('get_results/<str:room_name>', views.get_results, name='get_results'),
    path('control', views.control_cmd, name='pause'),
    path('test-students', views.create_test_students, name='test-students'),
    path('', views.index, name='teacher_index'),
    path('overview/', views.overview, name="overview"),
    path('overview/<str:room_name>', views.overview, name="overview"),
    path('create', views.create, name="create"),
]
