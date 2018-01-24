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
import update_config

'a script for build android package'

__author__ = 'sunshanming'

parser = argparse.ArgumentParser(description='a script for build android package')
parser.add_argument('--source', dest='source', help='android source path', required=True)
parser.add_argument('--config', dest='config', help='android config path', required=True)
parser.add_argument('-name', '--name', dest='name', default='NetworkSample' , help='project name')
parser.add_argument('-test', '--test', dest='test', action='store_true' , help='test apk build')
parser.add_argument('-doctor', '--doctor', dest='doctor', action='store_true' , help='doctor or patient')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print verbose logging.')

args = parser.parse_args()

verbose = args.verbose or False
parent_config = os.path.abspath(args.config)
source = os.path.abspath(args.source)
name = args.name
test = args.test or False
doctor = args.doctor or False

config = os.path.join(parent_config, 'resource')

if verbose:
    print 'parent config path: %s' % parent_config
    print 'config path: %s' % config
    print 'source path: %s' % source
    print 'name is: %s' % name

basename = os.path.basename(source)
app = os.path.join(source, name)
wx_activity_path = os.path.join(app, 'src/main/java/zj/health/zyyy/wxapi/WXPayEntryActivity.java')
config_path = os.path.join(app, 'src/main/java/com/example/networksample/ConfigConstant.java')
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
config_apk = os.path.join(os.path.abspath(os.path.join(config, '..')), 'apk/')

resource = {config_json_path, source, config, icon}


def add_x():
    subprocess.check_call('chmod +x %s' % gradlew, shell= True)


def check_config():
    # check resourde
    for p in resource:
        if not os.path.exists(p):
            raise ValueError('%s not exists' % p)
        else:
            if verbose:
                print 'config: %s' % p
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

def make_wx():
    wx_path = json_config_option.get('WX_CALLBACK')
    if wx_path and len(wx_path) > 0:
        package = json_config_data['prop_list']['ENVIRONMENT_PATIENT_ID']
        wx_store_path = os.path.join(app, wx_path)
        if not os.path.exists(wx_store_path):
            os.makedirs(wx_store_path)
            if verbose:
                print 'make wx dir: %s' % wx_store_path
        wx_maker.wx_cp(wx_activity_path, package, wx_store_path, verbose)
    else:
        print '没有发现微信回调,如果需要微信支付请选择'


def cp_resource():
    if verbose:
        print 'start cp resource'

    images.copy(config_image, [{'name': 'bg_welcome_background.png'}], default_res, verbose)


def update_prop():
    global json_config_data
    global json_config_option
    json_config_data = tools.load_json_from_file(config_json_path, verbose)

    if not json_config_data.has_key('option'):
        json_config_data['option'] = None

    data = json_config_data['prop_list']
    if doctor:
        data['ENVIRONMENT_PATIENT_FLAG'] = 'true'
    else:
        data['ENVIRONMENT_PATIENT_FLAG'] = 'false'
    json_config_option = json_config_data['option_list']
    update_properties.update_properties(data, gradle_path, config_apk, basename, test, verbose)


def make_key_store():
    key_store = json_config_option.get('key')
    if key_store and len(key_store) > 0:
        update_properties.update_key_store(tools.load_json_from_file(key_store, verbose), gradle_path, verbose)
    else:
        raise ValueError('没有配置证书,请选择证书')


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
        update_config.update_plist_option(json_config_data['option'], config_path, app, config_image, verbose)
    except Exception as e:
        print '更新配置失败'
        raise e

    try:
        make_wx()
    except Exception as e:
        print 'make wx error: message is : %s' % e.message
        raise e

    try:
        make_key_store()
    except Exception as e:
        print 'make key store: message is : %s' % e.message
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

    except Exception as e:
        print 'package error: message is : %s' % e.message


if __name__ == '__main__':
    main()

#