from django.http import HttpResponseBadRequest
from django.shortcuts import render, render_to_response


def index(request):
    return render(request, 'diceware/index.html')


def get_list(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    return render_to_response("diceware/dicewords.json", content_type='application/json')

