#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import argparse
import os
from utils import utils as tools
import requests
import datetime,time
import random
import re

'a script for upload apk or ipa to bugly'

__author__ = 'sunshanming'

parser = argparse.ArgumentParser(description='a script for upload apk or ipa to bugly')
parser.add_argument('--type', dest='type', help='app type, ios or android', default='android')
parser.add_argument('--source', dest='source', help='apk or ipa dir', required=True)
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print verbose logging.')

args = parser.parse_args()

verbose = args.verbose or False
type = args.type
source = os.path.abspath(args.source)

if verbose:
    print 'type: %s' % type
    print 'source: %s' % source

bugly_ids = None
if 'android' == type:
    bugly_ids = tools.load_json_from_file('./android.json')
else:
    bugly_ids = tools.load_json_from_file('./ios.json')


def upload(rawPath, updateDescription, config):
    print("Begin to upload ipa to bugly: %s" % rawPath)
    headers = {'enctype': 'multipart/form-data'}
    payload = {
        'app_id': config['app_id'],
        'pid': config['pid'],
        'title': updateDescription  # 版本更新描述
    }

    try_times = 0
    while try_times < 5:
        try:
            ipa_file = {'file': open(rawPath, 'rb')}
            resp = requests.post('https://api.bugly.qq.com/beta/apiv1/exp?app_key=%s' % config['app_key'],
                                 headers=headers, files=ipa_file, data=payload)
            assert resp.status_code == requests.codes.ok
            result = resp.json()
            if (result['rtcode'] == 0):
                print 'downLoadUrl: %s' % result['data']['url']
            print result
            return result
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError occured!")
            time.sleep(60)
            try_times += 1
        except Exception as e:
            print("Exception occured: %s" % str(e))
            time.sleep(60)
            try_times += 1

        if try_times >= 5:
            raise Exception("Failed to upload ipa to Pgyer, retried 5 times.")


index = random.randint(0, 5)

for file in os.listdir(source):
    if (re.match(r'.*-release.*', file)):
        upload(os.path.abspath(os.path.join(source, file)), 'test', bugly_ids[index])
        break