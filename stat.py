#!/bin/python2.7

import sys

odf_dir = "."
template = "template.ods"

#
# functions
#

def getdate():
    return False

def copy(src, dst):
    return False

def create_new_odf():
    date = getdate()
    copy(template, date + ".ods")
    return False

def read_odf(file):
    return False

def insert_row(odf, data):
    return False

def sort(odf):
    return False


#
# start
#

def main(argv):
    big_table = create_new_odf()

    for odf in odf_dir:
        data = read_odf(odf)
        insert_row(big_table, data)

    sort(big_table)

if __name__ == "__main__":
    main(sys.argv)
