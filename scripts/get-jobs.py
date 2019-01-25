# -*- coding: utf-8 -*-

import boto3
import json
import decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('test-jobs')


def generate_jobs_json():
    response = table.scan()
    jobs = replace_decimals(response['Items'])
    with open('_data/jobs.json', 'w') as outfile:
        json.dump(jobs, outfile)


# Workaround for decimals in DynamoDB
# https://github.com/boto/boto3/issues/369
def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


if __name__ == "__main__":
    generate_jobs_json()