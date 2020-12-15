# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:08:37 2020

@author: Gabriel
"""
import pygame
import sys
import logging

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        sys.stderr.write(data)
        sys.stderr.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

logging.basicConfig(filename='test.log', level=logging.DEBUG)
out = Unbuffered(sys.stdout)

"""print("test", file=out)
ligne = input()
logging.debug(ligne)"""

while True:
    ligne = input()
    logging.debug(ligne)