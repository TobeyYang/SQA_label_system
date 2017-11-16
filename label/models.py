import json

from django.db import models

# Create your models here.

MAX_UTTERANCE_LENGTH = 50
MAX_MENTION_LENGTH = 50
MAX_ANAPHORA_LENGTH = 20
MAX_ID_LENGTH = 10

class Query(models.Model):
    id = models.IntegerField(primary_key=True)
    utterance = models.TextField(max_length=MAX_UTTERANCE_LENGTH)
    mention = models.TextField(max_length=MAX_MENTION_LENGTH)
    # wiki_id = models.CharField(max_length=MAX_ID_LENGTH)
    follow_up = models.TextField(max_length=MAX_UTTERANCE_LENGTH, default="")
    anaphora_phrase = models.TextField(max_length=MAX_ANAPHORA_LENGTH, default="")
    follow_type = models.CharField(max_length=20, default=None)
    is_labeled = models.BooleanField(default=False)

    def __str__(self):
        return json.dump({'Q':self.utterance, 'M': self.mention, 'F': self.follow_up, 'A': self.anaphora_phrase})


# class Follow_up(models.Model):
#     query_id = models.IntegerField(primary_key=True)
#     follow_up_id = models.IntegerField(primary_key=True)
#     utterance = models.TextField(max_length=MAX_UTTERANCE_LENGTH)
#     anaphora_phrase = models.TextField(max_length=MAX_ANAPHORA_LENGTH)



