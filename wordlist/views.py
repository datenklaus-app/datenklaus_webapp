import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from wordlist.models import Words


class ALLWORDS:
    words = None


def index(request):
    if ALLWORDS.words is None:
        ALLWORDS.words = {}
        file = open("wordlist/wortliste_main", "r")
        ALLWORDS.words = file.read().split()

    word = None
    while True:
        word = random.choice(ALLWORDS.words)
        if Words.objects.filter(string=word).count() == 0 and len(word) < 10:
            break

    context = {"word": word, "count": Words.objects.all().count()}
    return render(request, "wordlist/index.html", context=context)


def yes(request, word):
    Words.objects.get_or_create(string=word)
    return HttpResponseRedirect(reverse("index"))


def no(request, word):
    return HttpResponseRedirect(reverse("index"))


def init(request):
    file = open("wordlist/wortliste_kinderlexikon", "r")
    kinderlexicon = file.read()
    kinderlexicon = kinderlexicon.replace('(', '')
    kinderlexicon = kinderlexicon.replace(')', '')
    words = []
    for word in kinderlexicon.split():
        o = Words.objects.get(string=word)
        o.delete()
    print(Words.objects.all())
    return HttpResponseRedirect(reverse("index"))


def save(request):
    file = open("wordlist/wortliste_final", "w")

    for word in Words.objects.all():
        file.write(word.string + "\n")

    return HttpResponseRedirect(reverse("index"))


def load(request):
    file = open("wordlist/wortliste_final", "r")

    for word in file.read().split():
        Words.objects.get_or_create(string=word)

    return HttpResponseRedirect(reverse("index"))
