# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:05:24 2017

@author: alan
"""

import os
import sys
'''
Move up in folder hierarchy (test/..) and add path to sys.path to access
mortgage package
'''
one_up_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if one_up_path not in sys.path:
    sys.path.append(one_up_path)