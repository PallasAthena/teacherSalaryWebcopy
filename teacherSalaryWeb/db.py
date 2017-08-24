#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 17:49:19 2017

@author: shaozl
"""

import pymysql.cursors

class DB:
    
    def __init__(self):
        try:
            self.connection = pymysql.connect(host='192.168.4.135',
                                              port=3306,
                                              user='biqiao',
                                              password='biqiao123',
                                              db='acornuser',
                                              charset='utf8mb4')
            
        except pymysql.err.OperationalError as e:
            print("mysql error {}, {}".format(e.args[0], e.args[1]))
            
    
    def select(self, sql):
        with self.connection.cursor() as cursor:
            if cursor.execute(sql):
                return cursor.fetchall()
            else:
                return None
            
            
    
            