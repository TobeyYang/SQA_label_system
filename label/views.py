# -*- encoding: utf8 -*-
import csv
import logging
import os

from django.http import JsonResponse
from django.shortcuts import render

from label.models import *


# Create your views here.





def get_home(request):
    '''
    return the home page contain a list of unlabeled queries.
    :param request:
    :return:
    '''
    pass


def statistics():
    sta = {}
    sta['labeled'] = len(FollowUp.objects.all())
    sta['anaphora_num'] = len(FollowUp.objects.filter(follow_type='Anaphora'))
    sta['ellipsis_num'] = len(FollowUp.objects.filter(follow_type='Ellipsis'))
    return sta


def get_query(request, query_id):
    print("get query: {}".format(query_id))
    query = Query.objects.get(id=query_id)
    table = query.target_table
    mentions = query.mention_set.all()

    query_info = {'id': query.id, 'utterance': query.utterance, 'parse_tree': query.parse_tree}

    follows_up_info = []
    for men in mentions:
        form_data = {}
        form_data['mention_id'] = men.id
        form_data['mention'] = men.mention

        follows = []
        for follow_up in men.followup_set.all():
            follow_data = {}
            follow_data['follow_id'] = follow_up.id
            follow_data['follow_up_type'] = follow_up.follow_type
            follow_data['transition_type'] = follow_up.transition_type
            follow_data['follow_up'] = follow_up.follow_up
            follow_data['anaphora_phrase'] = follow_up.anaphora_phrase
            follow_data['annotator'] = follow_up.annotator.name
            follows.append(follow_data)
        form_data['follows'] = follows
        follows_up_info.append(form_data)
    table_file = os.path.join(r'./table_csv', str(table.table_id) + '.csv')
    with open(table_file, 'r', encoding='utf8')as f:
        csv_reader = csv.reader(f)
        table_data = []
        for row in csv_reader:
            table_data.append(row)
    table_info = {'title': table.table_title, "rows": table_data}

    print(statistics())
    print(follows_up_info)
    return render(request, 'label.html', {
        'query_info': json.dumps(query_info),
        'follows_info': json.dumps(follows_up_info),
        # [{mention_id, mention, follows:[{follow_id, follow_up_type, ...},...]}]
        'table_info': json.dumps(table_info),
        'statistics_info': json.dumps(statistics())
    })


def get_unlabeled(request):
    pass


def get_next(request):
    logging.debug(request)
    json_data = json.loads(request.body.decode('utf8'))
    logging.debug(json_data)

    current_query_id = json_data['current_query_id']
    # current_query_id = 4
    next_id = current_query_id + 1
    return JsonResponse({'next_id': next_id})


def submit_data(request):
    logging.debug(request.body)

    json_data = json.loads(request.body.decode('utf8'))
    query_id = int(json_data['query_id'])
    mention = json_data['mention'].strip()
    follow_type = json_data['follow_up_type'].strip()
    transition_type = json_data['transition_type'].strip()
    follow_up = json_data['follow_up'].strip()
    anaphora_phrase = json_data['anaphora_phrase'].strip()
    annotator = Annotator.objects.get(id=1)

    valid, valid_mes = validation(follow_type, transition_type, follow_up, anaphora_phrase)

    if valid:
        query = Query.objects.get(id=query_id)
        mention_temp = Mention.objects.get_or_create(mention=mention, target_query=query)
        mention_message = "Mention: {} added.".format(json_data["mention"]) if mention_temp[
            1] else "Mention: {} exists."

        target_mention = mention_temp[0]
        target_mention.is_labeled = True
        target_mention.save()

        follow_up_temp = FollowUp.objects.get_or_create(
            target_mention=target_mention,
            follow_type=follow_type,
            transition_type=transition_type,
            follow_up=follow_up,
            anaphora_phrase=anaphora_phrase,
            annotator=annotator
        )
        follow_up_message = 'Follow Up: {} added.'.format(json_data['follow_up']) if follow_up_temp[
            1] else 'Do not submit it again.'
        message = mention_message + '\n' + follow_up_message
    else:
        message = valid_mes
    return JsonResponse({
        'message': message,
        'statistic_info': statistics()
    })


def validation(follow_type, transition_type, follow_up, anaphora_phrase):
    '''
    Determine if the submitted follow up is valid.
    :param follow_type:
    :param transition_type:
    :param follow_up:
    :param anaphora_phrase:
    :return:
    '''

    valid = False
    message = ""
    if follow_type == 'Ellipsis' and anaphora_phrase != '':
        message = 'Please check it. \nIn the condition of Ellipsis, the anaphora-phrase must be empty.'
    elif follow_type == 'Anaphora' and anaphora_phrase == '':
        message = 'Please check it. \nIn the condition of Anaphora, the anaphora-phrase can not be empty.'
    elif follow_type == 'Anaphora' and anaphora_phrase not in follow_up:
        message = 'Please check it. \nThe anaphora-phrase must be a substring of follow-up-query'
    else:
        valid = True
    return valid, message
