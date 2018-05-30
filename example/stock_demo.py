# encoding: utf-8

from opendatatools import stock

if __name__ == '__main__':

    index_list = stock.get_index_list('SZ')

    print(index_list)
