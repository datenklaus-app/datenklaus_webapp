from django.urls import path

from . import views

urlpatterns = [
    path('room/<room_name>', views.room, name='room'),
    path('', views.index, name='index'),
]
