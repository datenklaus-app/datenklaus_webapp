import collections
import random
from string import ascii_uppercase

from lexicon.models import LexiconEntry


def entry_titles_ordered() -> {str: [str]}:
    all_entries = collections.OrderedDict()

    for letter in ascii_uppercase:
        all_entries[letter] = []

    for entry in LexiconEntry.objects.all():
        all_entries[entry.title[0].upper()].append(entry.title)

    for letter in ascii_uppercase:
        if len(all_entries[letter]) == 0:
            del(all_entries[letter])
            continue
        all_entries[letter].sort()

    return all_entries


def get_random_entry() -> LexiconEntry:
    return random.choice(LexiconEntry.objects.all())
