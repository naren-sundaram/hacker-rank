import os
import csv
import json
import requests
from dateutil import parser
from datetime import datetime as dt


URL = 'http://mockbin.com/request'
HOME = os.environ['HOME']
FILE_PATH = HOME + '/Desktop/data.csv'


"""
0        1   2   3   4       5       6         7            8
Log ID	Key	Url	Id	Test	Code   Method	StartTime	LatencyMillseconds
"""


def csv_to_json():
    with open(FILE_PATH, 'r') as file_csv:
        data = []
        reader = csv.reader(file_csv, delimiter=',')

        for idx, row in enumerate(reader):
            if idx:
                category = "API Proxy" if row[4] == 'ApiRun' else row[4]
                task_name = "API_PROXY HTTP Operations Inline with JWT and Cert" \
                    if row[6] == 'GET' and row[4] == 'ApiRun' else row[1]
                latency = round(float(row[8]), 6)
                d = parser.parse(row[7].split(' UTC')[0])

                data.append({
                    '_id': row[1],
                    'category': category,
                    'for_date': dt.strftime(d.date(), '%Y-%m-%dT%H:%M:%SZ'),
                    "task_name": task_name,
                    "task_type": "TestTasks",
                    "latency": {
                        "avg": latency,
                        "max": latency,
                        "min": latency
                    },
                    "time": dt.strftime(d, '%Y-%m-%dT%H:%M:%SZ'),
                    "all_ids": [
                        {
                            "latency": str(latency),
                            "id": row[3],
                            "type": "org"
                        }
                    ],
                    "resource_id": "c1c2e017-4846-425b-a8e9-1972770ce0ee",
                    "log_id": row[0]
                })

            # if idx == 1:
            #     break

    return json.dumps(data)


def post_to_rserver(data_json):
    headers = {'content-type': 'application/json'}
    response = requests.post(URL + '/api/users', data=json.dumps(data_json), headers=headers)
    print(response)


def main():
    data_json = csv_to_json()
    print(data_json)
    post_to_rserver(data_json)


main()
