from django.urls import path

from . import views

urlpatterns = [
    path('', views.lesson, name='lesson'),
    path('next', views.lesson_next, name='lesson_next'),
    path('previous', views.lesson_previous, name='lesson_previous'),
    path('status', views.room_status, name='status')
]
