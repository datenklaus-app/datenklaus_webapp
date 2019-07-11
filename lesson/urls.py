from django.urls import path
from django.views.generic import TemplateView

from lesson.views import LineChartJSONView
from . import views

urlpatterns = [
    path('', views.lesson, name='lesson'),
    path('<int:state_num>', views.lesson, name='lesson'),
    path('chart', views.chart, name='chart'),
]