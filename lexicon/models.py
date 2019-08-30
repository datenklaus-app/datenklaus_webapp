import markdown
from django.db import models

# Create your models here.
from django.db.models import TextField
from markdown.extensions.wikilinks import WikiLinkExtension


class LexiconEntry(models.Model):
    title = TextField(primary_key=True)
    md = TextField()

    def as_html(self):
        return markdown.markdown(self.md,
                                 extensions=[WikiLinkExtension(base_url='/lexicon/', end_url='')])
