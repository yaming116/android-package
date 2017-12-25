#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'update config'

import images as icon_make
import utils.utils as tools
import re
import codecs
import os


def update_config(key, value, config_path, verbose):
    try:
        if verbose:
            print '开始更新配置文件'
        pattern = r'\b%s\b\s=[^"]{1}.*' % key
        result = '%s = %s;' % (key, value)

        data = tools.load_data_from_file(config_path, verbose)

        data = re.sub(pattern, result, data)

        with codecs.open(config_path, 'w', "utf-8") as header_file:
            header_file.write(data)
    except Exception as e:
        print '更新配置文件出错'
        raise e


def update_plist_option(options, config_path, source, resource, verbose):

    if not options:
        print 'option config is empty'
        return
    if verbose:
        print 'update option plist config'
        print '=========================='
        print options
    if options.has_key('HEAD_IMG') and options['HEAD_IMG']:
        print 'has HEAD_IMG'
        update_config('HOMEPAGETITLELOGO', '1', config_path, verbose)
        icon_make.head_ico_make(source, resource, verbose)
    else:
        print 'not found HEAD_IMG'
        update_config('HOMEPAGETITLELOGO', '0', config_path, verbose)

    if options.has_key('HOSPITAL_CONFIGURE') and options['HOSPITAL_CONFIGURE']:
        update_config('HOSPITAL_CONFIGURE', 'true', config_path, verbose)
    else:
        update_config('HOSPITAL_CONFIGURE', 'false', config_path, verbose)
    if options.has_key('HOSPITAL_AREA') and options['HOSPITAL_AREA']:
        update_config('HOSPITAL_AREA', 'true', config_path, verbose)
    else:
        update_config('HOSPITAL_AREA', 'false', config_path, verbose)

    if options.has_key('HOSPITAL_URL'):
        r = '"%s"' % options['HOSPITAL_URL']
        update_config('HOSPITAL_URL', r, config_path, verbose)


if __name__ == '__main__':
    path = os.path.join('.', 'A.java')
    r = '"%s"' % 'adb'
    update_config('HOSPITAL_URL', r, path, True)