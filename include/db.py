#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import Error
print("api level:",mysql.connector.apilevel)
print("paramstyle:",mysql.connector.paramstyle)

db=mysql.connector.connect(user='root',password='123456',host='localhost',port='3306',database='flow_db')
cursor=db.cursor()

