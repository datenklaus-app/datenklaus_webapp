import collections
import random
from string import ascii_uppercase

from lorem.text import TextLorem


class Lexicon:
    def __init__(self, generate_entries=False):
        self.entries = collections.OrderedDict()
        for letter in ascii_uppercase:
            self.entries[letter] = []
        if generate_entries:
            self.__generate_entries()

    class Entry:
        def __init__(self, title: str, description: str):
            self.title = title
            self.description = description.split()

        def __lt__(self, other):
            return self.title < other.title

        def __eq__(self, other):
            if type(other) is str:
                return self.title.lower() == other.lower()
            return self.title.lower() == other.title.lower()

    def __update_entries(self):
        all_entries = []
        for letter, entries in self.entries.items():
            self.entries[letter].sort()
            all_entries = all_entries + entries

        for entry in all_entries:
            for word in entry.description:
                if word[0] == '#':
                    continue

                if word in all_entries:
                    entry.description = [w.replace(word, '#' + word) for w in entry.description]

    def add(self, word, description):
        letter = str(word[0]).upper()
        if word in self.entries[letter]:
            self.entries[letter].remove(word)
            print(" kept: " + word)

        self.entries[letter].append(Lexicon.Entry(word, description))
        self.__update_entries()

    def get_random(self) -> Entry:
        entries = []
        while len(entries) <= 0:
            entries = random.choice(list(self.entries.values()))
        return random.choice(entries)

    def get(self, word) -> Entry:
        letter = str(word[0]).upper()
        if self.entries.get(letter) is None:
            return None
        try:
            return next(e for e in self.entries[letter] if e == word)
        except StopIteration:
            return None

    def __generate_entries(self):
        l = TextLorem(trange=(1, 1), prange=(1,5))
        for i in range(25):
            self.add(l.text().split()[0], l.paragraph())


dummy = Lexicon(generate_entries=True)