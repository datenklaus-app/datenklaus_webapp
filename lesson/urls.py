from django.urls import path

from . import views

urlpatterns = [
    path('', views.lesson, name='lesson'),
    path('<int:state_num>', views.lesson, name='lesson')
]