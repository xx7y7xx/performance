#!/bin/python2.7

odf_dir = "."

#
# functions
#

def create_new_odf():
    return False

def read_odf():
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
        data = read(odf)
        insert_row(big_table, data)

    sort(big_table)

if __name__ == "__main__":
    main(sys.argv)
