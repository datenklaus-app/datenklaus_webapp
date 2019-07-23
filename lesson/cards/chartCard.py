from django.shortcuts import render
from lesson.cards.card import Card


class ChartCard(Card):

    def __init__(self, state, title="Ergebnisse"):
        """
        :param labels: List of labels
        :param title: Card title
        :param colors: Optional color list
        """
        self.state = state
        self.title = title

    def render(self, request, context, chart=None):
        context["title"] = self.title
        context["cht"] = chart
        context["state"] = self.state
        return render(request, 'lesson/cards/chartCard.html', context=context)

    def post(self, post):
        pass
