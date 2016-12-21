#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'update properties'

from utils import utils
import codecs
import re


def update_properties(config_json_data, props_path, verbose = False):

    if verbose:
        print 'start update properties'

    data = utils.load_data_from_file(props_path, verbose)
    pattern = r'\%s\b\s=.*'

    for key, value in config_json_data.items():
        data = re.sub(pattern % key, '%s = %s' % (key, value), data)

    with codecs.open(props_path, 'w', "utf-8") as header_file:
        header_file.write(data)


if __name__ == '__main__':
    json = utils.load_json_from_file('./resource/config.json')
    properties_path = './Rubik3.0/app/gradle.properties'

    update_properties(json['prop_list'], properties_path, True)