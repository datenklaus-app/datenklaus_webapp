from django.shortcuts import render

from lesson.cards.card import Card


class ChartCard(Card):

    def __init__(self, title="Ergebnisse", template='lesson/cards/chartCard.html'):
        self.title = title
        self.template = template

    def render(self, request, context, chart=None):
        context["title"] = self.title
        context["cht"] = chart
        return render(request, self.template, context=context)

    def post(self, post):
        pass
