#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'update properties'

from utils import utils
import os
import codecs
import re
import time


def update_properties(config_json_data, props_path, config_apk, verbose = False):

    if verbose:
        print 'start update properties'

    data = utils.load_data_from_file(props_path, verbose)
    pattern = r'\%s\b\s=.*'

    for key, value in config_json_data.items():
        data = re.sub(pattern % key, '%s = %s' % (key, value), data)

    apk_path = config_json_data.get('APK_PATH')

    localtime = time.localtime(time.time())
    day = time.strftime("%Y-%m-%d", time.localtime())
    id = int(time.mktime(localtime) / 10)
    ipa_name = '%s_%s.apk' % (day, id)

    if not apk_path:
        value = os.path.join(config_apk, ipa_name)
        key = 'APK_PATH'
        config_json_data[key] = value
        data = re.sub(pattern % key, '%s = %s' % (key, value), data)
    else:
        pass

    with codecs.open(props_path, 'w', "utf-8") as header_file:
        header_file.write(data)


if __name__ == '__main__':
    json = utils.load_json_from_file('./resource/config.json')
    properties_path = './Rubik3.0/app/gradle.properties'

    update_properties(json['prop_list'], properties_path, os.path.abspath('./resource/apk'), True)
    print json['prop_list']['APK_PATH']