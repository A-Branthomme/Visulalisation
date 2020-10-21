#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 12:05:16 2020

@author: francoishervier
"""

import os
import json
import sys

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        #d['type'] = "file"
        d['value'] = os.path.getsize(path)
    return d

print (json.dumps(path_to_dict(sys.argv[1]),  indent=4))