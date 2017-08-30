#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'create app icon'

from os import path
import subprocess
import os
import shutil

drawables = [{'name': 'drawable-mdpi', 'size': 48} ,
             {'name': 'drawable-hdpi', 'size': 72} ,
             {'name': 'drawable-xhdpi', 'size': 96},
             {'name': 'drawable-xxhdpi', 'size': 144}]

cp_list = [{'name': 'ico_user_login_logo.png'},
           {'name' : 'bg_home_page_welcome_logo.png'}]


def make(icon, icon_dist, verbose, source = None):

    if verbose:
        print 'start make icon'

    command = 'convert -resize %sx%s  %s  %s'

    for drawable in drawables:
        name = drawable['name']
        size = drawable['size']

        icon_path = path.join(icon_dist, name);
        if not os.path.exists(icon_path):
            os.makedirs(icon_path)
        res_name = 'res_ic_launcher.png'
        if source == 'hospital' :
            res_name = 'ic_launcher.png'
        subprocess.check_call(command % (size, size, icon, path.join(icon_dist, name, res_name)), shell=True)


def check_images(image_resource, config_image_json, verbose):
    if verbose:
        print 'start check image file'

    if not config_image_json:
        config_image_json = cp_list
    for image in config_image_json:
        name = image['name']
        p = path.join(image_resource, name)
        if not (path.exists(p)):
            raise ValueError('image not exist: %s' % p)


def copy(image_resource, config_image_json, app_image_folder_dist, verbose):
    if verbose:
        print 'start image copy'

    if not config_image_json:
        config_image_json = cp_list
    for image in config_image_json:
        name = image['name']
        p = path.join(image_resource, name)
        if os.path.exists(p) :
            shutil.copy(p, app_image_folder_dist)
        else:
            print 'not found %s' % p


def head_ico_make(source, resource, verbose):
    if verbose:
        print 'update head ico'
    name = 'ico_home_page_title_logo.png'
    res = os.path.join(source, 'src', 'main', 'res')
    head_ico_path = os.path.join(res, 'drawable-hdpi')

    head_img = os.path.join(resource, 'ico_home_page_title_logo.png')
    if not os.path.exists(head_img):
        raise ValueError("医院logo图片没有上传")
    else:
        if verbose:
            print 'head image path is: %s' % head_img
            os.remove(os.path.join(head_ico_path, 'ico_home_page_title_logo.png'))

    p = path.join(head_ico_path, name)
    if os.path.exists(p):
        shutil.copy(p, head_ico_path)

if __name__ == '__main__':
    make(path.abspath('./resource/icon/icon.png'), path.abspath('./resource/test'), True)

