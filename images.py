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


def make(icon, icon_dist, verbose):

    if verbose:
        print 'start make icon'

    command = 'convert -resize %sx%s  %s  %s'

    for drawable in drawables:
        name = drawable['name']
        size = drawable['size']

        icon_path = path.join(icon_dist, name);
        if not os.path.exists(icon_path):
            os.makedirs(icon_path)

        subprocess.check_call(command % (size, size, icon, path.join(icon_dist, name, 'res_ic_launcher.png')), shell=True)


def check_images(image_resource, verbose):
    if verbose:
        print 'start check image file'

    for image in cp_list:
        name = image['name']
        p = path.join(image_resource, name)
        if not (path.exists(p)):
            raise ValueError('image not exist: %s' % p)


def copy(image_resource, app_image_folder_dist, verbose):
    if verbose:
        print 'start image copy'
    for image in cp_list:
        name = image['name']
        p = path.join(image_resource, name)
        shutil.copy(p, app_image_folder_dist)


if __name__ == '__main__':
    make(path.abspath('./resource/icon/icon.png'), path.abspath('./resource/test'), True)