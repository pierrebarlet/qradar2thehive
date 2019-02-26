#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from thehive4py.api import *
from thehive4py.models import *
from thehive4py.query import *
import json

api = TheHiveApi('http://localhost:9000', '**YOUR_API_KEY**')


def search(title, query, range, sort):
    print(title)
    print('-----------------------------')
    response = api.find_cases(query=query, range=range, sort=sort)
    case = response.json()
    # If you want to update customfields:
    #customFields = CustomFieldHelper()\
    #   .add_string('**custom_fields_to_update**', "**new_value**")\
    #   .build()
    if response.status_code == 200: 
       var=case[0]["id"]
       print(var)
       # attributes to update
       updated_case = api.case.update(var,
                               status='Resolved',
                               resolutionStatus='TruePositive',
                               impactStatus='NoImpact',
                               summary='case closed by api',
                               owner='MyName',
                               #customFields=customFields,
                               )
    else:
        print('ko: {}/{}'.format(response.status_code, response.text))
        sys.exit(0)
# Range of cases to update:
for i in range(**min_case_id_to_update**,**max_case_id_to_update**):
        search("List cases", Eq('caseId', i), 'all', [])
