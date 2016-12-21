#!/usr/bin/env python
# _*_ coding: utf-8 _*_

def str_to_ucps(s):
    '''Translate a str object into a raw escaped unicode string literal.'''
    return ''.join(hex(ord(c)).replace('0x', r'\u') for c in s)


