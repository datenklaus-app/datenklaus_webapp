from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select_room/', views.select_room, name='select_room'),
    path('join/', views.join_room, name='join'),
    path('leave/', views.leave_room, name='leave'),
]
