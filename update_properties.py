#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'update properties'

from utils import utils
import os
import codecs
import re
import time


def update_properties(config_json_data, props_path, config_apk, basename, test, verbose = False):

    if verbose:
        print 'start update properties'

    data = utils.load_data_from_file(props_path, verbose)
    pattern = r'\b%s\b\s=.*'

    for key, value in config_json_data.items():
        data = re.sub(pattern % key, r'%s = %s' % (key, value), data)
    http_path = config_json_data.get('TEST_HTTP_PATH', None)
    apk_path = config_json_data.get('APK_PATH')

    if test :
        if http_path and len(http_path) > 0:
            key = u'HTTP_PATH'
            value = http_path
            data = re.sub(pattern % key, r'%s = %s' % (key, value), data)
        else:
            raise ValueError('test http path not found')
    else:
        http_path = config_json_data.get('HTTP_PATH', '')

    update_rubik_x_http(os.path.dirname(props_path), http_path, verbose)

    localtime = time.localtime(time.time())
    day = time.strftime("%Y-%m-%d_%H:%M", time.localtime())
    id = int(time.mktime(localtime) / 10)
    if test:
        ipa_name = '%s_%s_test_%s.apk' % (day, id, basename)
    else:
        ipa_name = '%s_%s_%s.apk' % (day, id, basename)

    if not apk_path or len(apk_path) <= 0 :
        value = os.path.join(config_apk, ipa_name)
        key = u'APK_PATH'
        config_json_data[key] = value
        data = re.sub(pattern % key, r'%s = %s' % (key, value), data)
    else:
        pass

    with codecs.open(props_path, 'w', "utf-8") as header_file:
        header_file.write(data)


def update_rubik_x_http(basepath, http_path, verbose=False):
    http_config = os.path.join(basepath, 'src', 'main', 'assets', 'http_config.xml')

    if not os.path.exists(http_config):
        print 'http_config.xml not found'
        return

    data = utils.load_data_from_file(http_config, verbose)

    pattern = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    data = re.sub(pattern, http_path, data)

    with codecs.open(http_config, 'w', "utf-8") as header_file:
        header_file.write(data)


if __name__ == '__main__':
    json = utils.load_json_from_file('./resource/config.json')
    properties_path = './Rubik3.0/app/gradle.properties'

    update_properties(json['prop_list'], properties_path, os.path.abspath('./resource/apk'), True)
    print json['prop_list']['APK_PATH']