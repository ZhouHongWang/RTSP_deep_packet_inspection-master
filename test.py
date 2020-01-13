#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import threading

c=[20153,20134]
b=[20155,20136]
for x in c:
    if x not in b:
        b.append(x)
print(b)
print(threading.active_count())
print(threading.enumerate())