#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'update config'

import images as icon_make
import utils.utils as tools
import re
import codecs


def update_config(key, value, config_path, verbose):
    try:
        if verbose:
            print '开始更新配置文件'
        pattern = '\b%s\b\s=[^"]{1}.*' % key
        result = '%s = %s;' % (key, value)

        data = tools.load_data_from_file(config_path, verbose)

        data = re.sub(pattern, value, data)

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