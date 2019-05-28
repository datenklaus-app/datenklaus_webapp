from django.shortcuts import render


def index(request):
    if request.session.is_empty():
        request.session.create()
    return render(request, 'index/index.html')
