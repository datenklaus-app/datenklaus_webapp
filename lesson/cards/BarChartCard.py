import pygal
from django.shortcuts import render
from pygal.style import DefaultStyle

from lesson.cards.card import Card


class BarChartCard(Card):

    def __init__(self, state, labels, title="Ergebnisse"):
        """
        :param labels: List of labels
        :param title: Card title
        :param colors: Optional color list
        """
        self.state = state
        self.title = title
        self.labels = labels

    def render(self, request, context, dataset=[]):
        style = DefaultStyle()
        style.background = "#FFFFFF"
        chart = pygal.Bar(show_legend=False, show_y_labels=True,
                          classes=(..., "card-img-bottom", "img-fluid"),
                          style=style, height=450)
        chart.x_labels = self.labels
        chart.y_labels = range(max(dataset) + 1)

        chart.add('', dataset)
        context["title"] = self.title
        context["cht"] = chart.render(is_unicode=True)
        context["state"] = self.state
        return render(request, 'lesson/cards/barChartCard.html', context=context)

    def handle_post(self, post):
        pass
