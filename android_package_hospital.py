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
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print verbose logging.')

args = parser.parse_args()

verbose = args.verbose or False
parent_config = os.path.abspath(args.config)
source = os.path.abspath(args.source)
name = args.name

config = os.path.join(parent_config, 'resource')

if verbose:
    print 'parent config path: %s' % parent_config
    print 'config path: %s' % config
    print 'source path: %s' % source
    print 'name is: %s' % name

basename = os.path.basename(source)
app = os.path.join(source, name)
res = os.path.join(app, 'src', 'flavors_patient', 'res')
res_2 = os.path.join(app, 'src', 'flavors_doctor', 'res')
default_res = os.path.join(res, 'drawable-hdpi')
default_res_2 = os.path.join(res_2, 'drawable-hdpi')
gradlew = os.path.join(source, 'gradlew')
gradle_path = os.path.join(source, 'gradle.properties')

json_config_data = None
json_config_option = None
json_config_image_data = None

config_json_path = os.path.join(config, 'config.json')
icon = os.path.join(config, 'icon', 'icon1.png')
icon_2 = os.path.join(config, 'icon', 'icon2.png')
config_image = os.path.join(config, 'images')
config_image_path = os.path.join(source, 'config.json')
config_apk = os.path.join(os.path.abspath(os.path.join(config, '..')), 'apk')

def add_x():
    subprocess.check_call('chmod +x %s' % gradlew, shell= True)


def check_config():
    if verbose:
        print 'start check config'

    #
    if not os.path.exists(config_apk):
        os.makedirs(config_apk)


def make_icon():
    if verbose:
        print 'start make icon'

    if os.path.exists(icon) :
        images.make(icon, res, verbose, 'hospital')
    else:
        print 'not found icon1.png,path: %s' % icon

    if os.path.exists(icon_2):
        images.make(icon_2, res_2, verbose, 'hospital')
    else:
        print 'not found icon2.png, path: %s' % icon_2


def cp_resource():
    if verbose:
        print 'start cp resource'

    images.copy(config_image, [{'name': 'bg_welcome_background1.png'}], default_res, verbose)
    images.copy(config_image, [{'name': 'bg_welcome_background2.png'}], default_res_2, verbose)


def update_prop():
    global json_config_data
    global json_config_option
    json_config_data = tools.load_json_from_file(config_json_path, verbose)

    data = json_config_data['prop_list']
    apk_path = data.get('APK_PATH')
    if not apk_path or len(apk_path) <= 0 :
        data['APK_PATH'] = config_apk
    update_properties.update_properties(data, gradle_path, config_apk, basename, False, verbose)


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