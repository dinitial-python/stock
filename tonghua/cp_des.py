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

# 
# return description of the stock
#
def get_stock_description(stock, file):
    wBook = xlrd.open_workbook(file)
    wSheet = wBook.sheets()[0]
    
    # total line of the excel
    totalRow = wSheet.nrows    

    # index from first row
    nRow = 0

    while True:
        if nRow >= totalRow:
            break

        code = wSheet.cell(nRow, 1).value
        if code == stock:        
            return wSheet.cell(nRow, 5).value

        nRow += 1

    return None

# 
# add new stock to the reference description file
#
def add_stock_to_description(val00, val01, val02, val03, file):
    wBook = xlrd.open_workbook(file)
    totalRow = wBook.sheets()[0].nrows
    
    writeBook = copy(wBook)
    wooksheet = writeBook.get_sheet(0)

    # index to the next line, excel index from zero
    wooksheet.write(totalRow, 0, val00)
    wooksheet.write(totalRow, 1, val01)
    wooksheet.write(totalRow, 2, val02)
    wooksheet.write(totalRow, 3, val03)

    writeBook.save(file)

#
# 功能：为文件 file1 中的股票添加描述符。描述符的参考文件为 file2，写入到新创建的 file3 中
#
# help information
print("python  agu.py  file1 file2 file3")

#
# 思路：
# 1.从 file1 中读取股票代码，直到 file1 的最后一行为止
# 2.检查该股票代码是否在 file2 中，如果在 file2 中则返回描述符，否则返回 null
# 3.如果该股票在 file2 中，则将描述符写入 file3 中，否则写入不带描述符的信息
#

param1 = sys.argv[1]
param2 = sys.argv[2]
param3 = sys.argv[3]

print(param1)
print(param2)
print(param3)

# file1 to read
wBook = xlrd.open_workbook(param1)
wSheet = wBook.sheets()[0]
    
# total line of the excel
totalRow = wSheet.nrows    

# index from first row
nRow = 1

# file3 to write
wb = xlwt.Workbook()
ws = wb.add_sheet('agu')

while True:
    if nRow >= totalRow:
        break

    val0 = wSheet.cell(nRow, 0).value
    ws.write(nRow, 0, val0)

    val1 = wSheet.cell(nRow, 1).value
    ws.write(nRow, 1, val1)

    val2 = wSheet.cell(nRow, 2).value
    ws.write(nRow, 2, val2)

    val3 = wSheet.cell(nRow, 3).value
    ws.write(nRow, 3, val3)

    code = wSheet.cell(nRow, 0).value
    des = get_stock_description(code, param2)    
    if des!=None:        
        ws.write(nRow, 4, des)
    else:
        add_stock_to_description(val0, val1, val2, val3, param2)

    nRow += 1

    print("nRow val is:" + str(nRow))

wb.save(param3)