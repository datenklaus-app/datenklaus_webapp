import os

from django.core.management.base import BaseCommand, CommandError

from lexicon.models import LexiconEntry


class Command(BaseCommand):
    help = 'Load entries from filesystem into database'

    def handle(self, *args, **options):

            for filename in os.listdir("lexicon/entries"):
                with open("lexicon/entries/" + os.fsdecode(filename), 'r') as file:
                    title = os.fsdecode(filename).split('.')[0]
                    print("Reading: " + title + "..")
                    md = file.read()
                    LexiconEntry.objects.get_or_create(title=title, md=md)

