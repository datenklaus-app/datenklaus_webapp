import json

from django.shortcuts import render

def index(request):
    # TODO: check for existing session
    # Make sure session Id is assigned
    request.session.save()
    return render(request, 'index/index.html')
