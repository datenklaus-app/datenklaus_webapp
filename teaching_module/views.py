from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('teaching_module/index.html')
    context = {}
    return HttpResponse(template.render(context, request))