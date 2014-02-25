# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 23:00:01 2014

@author: Ella
"""
import data_set
if __name__ == "__main__":
    ds = data_set.DataSet()
    for i in range(5):
        print ds.get_next_data()