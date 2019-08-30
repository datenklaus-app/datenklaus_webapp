import collections
import random

from lexicon.models import LexiconEntry


def entry_titles_ordered() -> {str: [str]}:
    all_entries = collections.OrderedDict()

    for entry in LexiconEntry.objects.all():
        letter = entry.title[0].upper()

        if letter not in all_entries.keys():
            all_entries[letter] = []

        all_entries[letter].append(entry.title)

    for letter in all_entries.keys():
        all_entries[letter].sort()

    return all_entries


def get_random_entry() -> LexiconEntry:
    return random.choice(LexiconEntry.objects.all())
