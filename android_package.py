#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import argparse
import os
import subprocess
import time

import utils.utils as tools
import shutil
import images
import update_properties
import wx_maker

'a script for build android package'

__author__ = 'sunshanming'

parser = argparse.ArgumentParser(description='a script for build android package')
parser.add_argument('--source', dest='source', help='android source path', required=True)
parser.add_argument('--config', dest='config', help='android config path', required=True)
parser.add_argument('-name', '--name', dest='name', default='app' , help='project name')
parser.add_argument('-test', '--test', dest='test', action='store_true' , help='test apk build')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print verbose logging.')

args = parser.parse_args()

verbose = args.verbose or False
test = args.test or False
parent_config = os.path.abspath(args.config)
source = os.path.abspath(args.source)
name = args.name

config = os.path.join(parent_config, 'resource')

if verbose:
    print 'parent config path: %s' % parent_config
    print 'config path: %s' % config
    print 'source path: %s' % source
    print 'is test: %s' % test
    print 'name is: %s' % name

basename = os.path.basename(source)
app = os.path.join(source, name)
wx_activity_path = os.path.join(app, 'src/main/java/com/rubik/demo/patient/wxapi/WXPayEntryActivity.java')
res = os.path.join(app, 'src', 'main', 'res')
default_res = os.path.join(res, 'drawable-hdpi')
gradlew = os.path.join(source, 'gradlew')
gradle_path = os.path.join(app, 'gradle.properties')

json_config_data = None
json_config_option = None
json_config_image_data = None

config_json_path = os.path.join(config, 'config.json')
icon = os.path.join(config, 'icon', 'icon.png')
config_image = os.path.join(config, 'images')
config_image_path = os.path.join(source, 'config.json')
config_apk = os.path.join(os.path.abspath(os.path.join(config, '..')), 'apk')


resource = {config_json_path, source, config, icon}


def add_x():
    subprocess.check_call('chmod +x %s' % gradlew, shell= True)


def check_config():
    if verbose:
        print 'start check config'

    # check resourde
    for p in resource:
        if not os.path.exists(p):
            raise ValueError('%s not exists' % p)
        else:
            if verbose:
                print 'config: %s' % p

    # load bundle json data
    if os.path.exists(config_image_path):
        data = tools.load_json_from_file(config_image_path)
        global json_config_image_data
        json_config_image_data = data
    else:
        if verbose:
            print 'not found %s' % config_image_path

    # check image resource
    images.check_images(config_image, json_config_image_data, verbose)

    #
    if not os.path.exists(config_apk):
        os.makedirs(config_apk)


def make_icon():
    if verbose:
        print 'start make icon'

    images.make(icon, res, verbose)


def cp_resource():
    if verbose:
        print 'start cp resource'

    images.copy(config_image, json_config_image_data, default_res, verbose)


def update_prop():
    global json_config_data
    global json_config_option
    json_config_data = tools.load_json_from_file(config_json_path, verbose)

    data = json_config_data['prop_list']
    json_config_option = json_config_data['option_list']
    update_properties.update_properties(data, gradle_path, config_apk, basename, test, verbose)


def make_wx():
    wx_path = json_config_option.get('WX_CALLBACK')
    if wx_path and len(wx_path) > 0:
        package = json_config_data['prop_list']['PACKAGE_NAME']
        wx_store_path = os.path.join(app, wx_path)
        if not os.path.exists(wx_store_path):
            os.makedirs(wx_store_path)
            if verbose:
                print 'make wx dir: %s' % wx_store_path
        wx_maker.wx_cp(wx_activity_path, package, wx_store_path, verbose)
    else:
        print 'not found wx call back'


def main():

    try:
        check_config()
    except Exception as e:
        print 'check config error, message is : %s' % e.message
        raise e

    try:
        make_icon()
    except Exception as e:
        print 'make icon error: message is : %s' % e.message
        raise e

    try:
        cp_resource()
    except Exception as e:
        print 'copy resource error: message is : %s' % e.message
        raise e

    try:
        update_prop()
    except Exception as e:
        print 'update prop error: message is : %s' % e.message
        raise e

    try:
        make_wx()
    except Exception as e:
        print 'make wx error: message is : %s' % e.message
        raise e

    try:
        add_x()
    except Exception as e:
        print 'add chmod exception , message is : %s' % e.message
        raise e

    try:
        command = 'cd %s && %s clean aR' % (source, gradlew)
        if verbose:
            print 'package command %s' % command
        subprocess.check_call(command, shell=True)

        apk = json_config_data['prop_list']['APK_PATH']

        print '======================================='
        print 'app_path: %s' % apk
        print '======================================='
    except Exception as e:
        print 'package error: message is : %s' % e.message


if __name__ == '__main__':
    main()

#