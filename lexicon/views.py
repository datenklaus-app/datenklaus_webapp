from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lexicon import lexiconUtils
from lexicon.models import LexiconEntry


def index(request):
    context = {"lexicon": lexiconUtils.entry_titles_ordered().items()}
    return render(request, "lexicon/index.html", context=context)


def random(request):
    return HttpResponseRedirect(reverse("lex_entry", args=[lexiconUtils.get_random_entry().title]))


def display_entry(request, title):
    try:
        entry = LexiconEntry.objects.get(title=title)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    return render(request, "lexicon/entry.html",
                  context={"entry": entry.as_html()})
