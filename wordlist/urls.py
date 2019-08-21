from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yes/<str:word>', views.yes, name='yes'),
    path('no/<str:word>', views.no, name='no'),
    path('save', views.save, name='save'),
]
