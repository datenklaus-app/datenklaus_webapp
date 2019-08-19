from django.shortcuts import render

from lesson.cards.card import Card


class ChartCard(Card):

    def __init__(self, state, title="Ergebnisse", template='lesson/cards/chartCard.html'):
        self.state = state
        self.title = title
        self.template = template

    def render(self, request, context, chart=None):
        context["title"] = self.title
        context["cht"] = chart
        context["state"] = self.state
        return render(request, self.template, context=context)

    def post(self, post):
        pass
