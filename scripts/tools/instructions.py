# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 17:42:52 2014

Read written instructions from an instructions text file. 

@author: smathias
"""
import os

def read_instructions(*args):
    p = os.path.join(os.path.dirname(os.getcwd()), 'instructions')
    txt = open(os.path.join(p, '%s_%s.txt' %args)).read()
    return [s.strip('\n') for s in txt.split('---')]