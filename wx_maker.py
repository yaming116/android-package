#!/usr/bin/env python
# _*_ coding: utf-8 _*_


# app/src/main/java/com/rubik/demo/patient/wxapi/WXPayEntryActivity.java

from utils import utils
import re
import codecs
from os import path
import os


def wx_cp(path, package_name, store_path, verbose=False):

    if verbose:
        print 'start maker wx support file'

    data = utils.load_data_from_file(path)

    pattern = r'^\bpackage\b.*'
    value = 'package %s.wxapi;' % package_name;
    data = re.sub(pattern, value, data)
    wx_file = os.path.join(store_path, 'WXPayEntryActivity.java')
    with codecs.open(wx_file, 'w', "utf-8") as wx_file:
        wx_file.write(data)


if __name__ == '__main__':

    p = './Rubik3.0/app/src/main/java/com/rubik/demo/patient/wxapi/WXPayEntryActivity.java'

    s = path.join('./Rubik3.0/app/src/main/java/com/rubik/test/patient/wxapi/')

    os.makedirs(s)

    wx_cp(p, 'com.test', './Rubik3.0/app/src/main/java/com/rubik/test/patient/wxapi/WXPayEntryActivity.java')