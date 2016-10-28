#!/usr/bin/python

import sys
import operator

def calc_gain(open_value, close_value):
    gain = close_value - open_value
    if gain < 0:
        gain = 0
    return gain

def calc_loss(open_value, close_value):
    loss = open_value - close_value
    if loss < 0:
        loss = 0
    return loss

def calc_mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
