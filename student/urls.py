from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join_room, name='join')
    # path('poll/<int:question_id>', views.poll, name='poll'),
    # path('poll/<int:question_id>/results', views.poll_results, name='poll_results'),
    # path('poll/<int:question_id>/vote/<int:choice_id>', views.poll_vote, name='poll_vote'),
]