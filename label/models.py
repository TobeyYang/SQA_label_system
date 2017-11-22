import json

from django.db import models

# Create your models here.

MAX_UTTERANCE_LENGTH = 50
MAX_MENTION_LENGTH = 50
MAX_ANAPHORA_LENGTH = 20
MAX_ID_LENGTH = 10
MAX_NAME_LENGTH = 20
MAX_PASSWORD_LENGTH = 20


class Annotator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Table(models.Model):
    # id = models.AutoField(primary_key=True)
    table_id = models.CharField(max_length=20, primary_key=True)  # like 200_34
    table_title = models.TextField(default='')

class Query(models.Model):
    id = models.AutoField(primary_key=True)
    target_table = models.ForeignKey(Table)
    utterance = models.TextField(max_length=20)
    parse_tree = models.TextField()


class Mention(models.Model):
    id = models.AutoField(primary_key=True)
    target_query = models.ForeignKey(Query)
    mention = models.TextField(default='')
    semantic_hint = models.TextField(default='')
    is_labeled = models.BooleanField(default=False)


class FollowUp(models.Model):
    id = models.AutoField(primary_key=True)
    target_mention = models.ForeignKey(Mention)
    follow_type = models.CharField(max_length=20, default="")
    transition_type = models.CharField(max_length=20, default="")
    follow_up = models.TextField(max_length=MAX_UTTERANCE_LENGTH, default="")
    anaphora_phrase = models.TextField(max_length=MAX_ANAPHORA_LENGTH, default="")
    annotator = models.ForeignKey(Annotator)
