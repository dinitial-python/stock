#
# 把 excel 件中的字符串小写转换为大写到新的文件中
#
# 例如：将 SH600025 转换为 sh600025
# 

# solve the problem with print ...
import pandas as pd
# import akshare tools
import akshare as ak
# get the line
import linecache
# write excel
import xlwt
# read excel
import xlrd

from xlutils.copy import copy
# get line number
import sys

# get time
import time

import os


def get_stock_description(rd_file, wr_file):

    # 写入的文件
    wb = xlwt.Workbook()
    ws = wb.add_sheet('agu')

    rdBook = xlrd.open_workbook(rd_file)
    rdSheet = rdBook.sheets()[0]

    # total line of the rd excel
    totalRow = rdSheet.nrows

    # index from first row
    nRow = 0

    while True:
        if nRow >= totalRow:
            break

        val = rdSheet.cell(nRow, 0).value
        ws.write(nRow, 0, val)

        val = rdSheet.cell(nRow, 1).value
        bigVal = val.upper()
        ws.write(nRow, 1, bigVal)

        val = rdSheet.cell(nRow, 2).value
        ws.write(nRow, 2, val)

        val = rdSheet.cell(nRow, 3).value
        ws.write(nRow, 3, val)

        val = rdSheet.cell(nRow, 4).value
        ws.write(nRow, 4, val)

        val = rdSheet.cell(nRow, 5).value
        ws.write(nRow, 5, val)

        nRow += 1
    
    wb.save(wr_file)

#
# 功能：将文件 file2s 中的股票描述输入到 file1 中
#
# help information
print("python  agu.py  file1 file2")

param1 = sys.argv[1]
param2 = sys.argv[2]

print(param1)
print(param2)

get_stock_description(param1, param2)