# python3
# -*-coding: utf8 -*-
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SQA_label_system.settings')
django.setup()


def main(data_file):
    from label.models import Annotator, Table, Query, Mention, FollowUp
    with open(data_file, 'r', encoding='utf8')as f:
        import_data = json.load(f)

    for data_item in import_data[:20]:
        table_id = data_item['table']
        utterance = data_item['Utterance']
        parse_tree = data_item['Binding']
        table = Table.objects.get_or_create(table_id=table_id, table_title=table_id + " test")[0]
        print(table)
        query = Query.objects.get_or_create(target_table=table, utterance=utterance, parse_tree=parse_tree)[0]

        mentions = data_item['mentions']
        for men in mentions:
            Mention.objects.get_or_create(target_query=query, mention=' '.join(men['mention']),
                                          semantic_hint='hint test')


if __name__ == '__main__':
    data_file = 'data_v1.txt'
    main(data_file)
    print('Bingo!')
