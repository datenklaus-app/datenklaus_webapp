from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='lexicon_index'),
    path('!', views.random, name='random'),
    path('<str:title>', views.display_entry, name='lex_entry'),
]
