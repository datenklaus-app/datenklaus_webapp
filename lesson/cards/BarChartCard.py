import chartjs
import pygal
from django.shortcuts import render
from pygal.style import DefaultStyle

from lesson.cards.card import Card


class LineChartCard(Card):

    def __init__(self, labels, title="Ergebnisse", colors=chartjs.colors.COLORS):
        """
        :param labels: List of labels
        :param title: Card title
        :param colors: Optional color list
        """
        self.colors = colors
        self.title = title
        self.labels = labels

    def render(self, request, context, dataset=[]):
        style = DefaultStyle()
        style.background = "#FFFFFF"
        chart = pygal.Bar(show_legend=False, show_y_labels=True, height=300, style=style)
        chart.x_labels = self.labels
        chart.y_labels = range(max(dataset)+1)
        chart.add('', dataset)
        context["title"] = self.title
        context["cht"] = chart.render(is_unicode=True)
        return render(request, 'lessons/cards/barChartCard.html', context=context)

    def handle_post(self, post, student):
        pass
