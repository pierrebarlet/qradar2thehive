#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import json
import requests
import warnings
import json
import time
import uuid
import sys
import hashlib
import time
from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CustomFieldHelper, CaseTask, CaseObservable

#To use this script correctly please configure the following lines
file_id = "</path/to/id_file.txt>"
api = TheHiveApi('<URL_THE_HIVE>', '<THE_HIVE_API_KEY>')
warnings.filterwarnings('ignore')
url = 'https://<QRadar_IP_address>/api/siem/offenses?fields=id%2Cstatus%2Cdescription%2Coffense_type%2Coffense_source%2Cmagnitude%2Csource_network%2Cdestination_networks%2Cassigned_to%2Cstart_time%2Cevent_count'
headers = {'accept': 'application/json', 'SEC': '<QRADAR_API_KEY>', 'Version': '9.0'}

#If you're using a selfsigned certificate on your QRadar instance you have to use "verify=false" parameter:
response_1 = requests.get(url,headers=headers,verify=False)

tasks = [
    CaseTask(title='Tracking'),
    CaseTask(title='Communication'),
    CaseTask(title='Investigation', status='Waiting', flag=True)
]

if (response_1.status_code) == 200:
    data = response_1.json()
    last_id = (str((data[0]['id'])))
    
    with open(file_id) as f:
        data_file = f.readlines()
        last_line = data_file[-1]
   
    if int(last_line) < int(last_id):
        first_new_offense = int(last_line)
        file = open(file_id, "w")
        file.write(last_id)
        file.close()
        diff = int(last_id) - first_new_offense
        
        for i in range(0,diff):
            offenseId = int(data[i]['id'])
            offenseDescription = str(data[i]['description'])
            offenseSource = str(data[i]['offense_source'])
            offenseMagnitude = int(data[i]['magnitude'])
            offenseSourceNetwork = str(data[i]['source_network'])
            offenseDestinationNetworks = str(data[i]['destination_networks'])
            offenseEventCount = int(data[i]['event_count'])
            
            #To use the following custom fields you have to create them on The Hive with the same internal reference (offenseId,...) and the same type (number,string...)
            #.add_<type>('<internal reference>', <value>)
            customFields = CustomFieldHelper()\
                .add_number('offenseId', offenseId)\
                .add_number('offenseMagnitude', offenseMagnitude)\
                .add_number('offenseEventCount', offenseEventCount)\
                .add_string('offenseSource', offenseSource)\
                .add_string('offenseSourceNetwork', offenseSourceNetwork)\
                .add_string('offenseDestinationNetworks', offenseDestinationNetworks)\
                .add_string('reasonForClosing', "null")\
                .build()
            
            case = Case(title=offenseDescription,
                tlp=3,
                flag=True,
                tags=['offense', 'qradar'],
                description=offenseDescription,
                tasks=tasks,
                customFields=customFields)
            
            id = None
            response_2 = api.create_case(case)
            
            if response_2.status_code == 201:
                id = response_2.json()['id']
            
            else:
                print('ko: {}/{}'.format(response_2.status_code, response_2.text))
                sys.exit(0)
            
            #Observables can be use with Cortex's analyzers
            source_ip_observable = CaseObservable(dataType='ip',
                                    data=[str(data[i]['offense_source'])],
                                    tlp=3,
                                    ioc=True,
                                    tags=['Source IP'],
                                    message="Offense source IP"
                                    )
            
            response_3 = api.create_case_observable(id, source_ip_observable)
            
            if response_3.status_code == 201:
                id = response_3.json()['id']
            
            else:
                print('ko: {}/{}'.format(response_3.status_code, response_3.text))
                sys.exit(0)
    
    else:
        diff = int(last_id) - int(last_line)
        print(str(diff) + " new offenses.")

else:
    print("Can't get offenses, check the configuration.")
