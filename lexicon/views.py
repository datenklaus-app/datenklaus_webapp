from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lexicon.lexicon import dummy


def index(request):
    context = {"lexicon": dummy.entries.items()}
    return render(request, "lexicon/index.html", context=context)


def random(request):
    return HttpResponseRedirect(reverse("lex_entry", args=[dummy.get_random().title]))


def display_entry(request, title):
    entry = dummy.get(title)

    if entry is None:
        return HttpResponseNotFound()

    return render(request, "lexicon/entry.html",
                  context={
                      "title": entry.title,
                      "description": entry.description,
                  })
