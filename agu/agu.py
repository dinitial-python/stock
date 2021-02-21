#
# 1.支持“黑名单”，用来过滤不需要的检查的股票
# 2.支持命令行输出，命令：python agu.py [testdir] [platform]
#   - testdir: 表示 test 目录中是否包含了股票的价格列表，其值为 "have" 或 "no"
#   - platform: 表示该 python 脚本运行的平台，可以是 "winddows" 或 "linux"
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

def info(info):
    print(str(sys._getframe().f_lineno) + info)

# get the line content
def get_line_content(file_path, line_number):
    return linecache.getline(file_path, int(line_number)).strip()

#
# 返回 bool 变量，表示指定的股票代码是否列入了黑名单
# True 表示找到了，False 表示没有找到
#
def checkBlackList(stock, name):
    file = open(name,'r', encoding='UTF-8')

    while True:
        line = file.readline()
        if not line:
            break

        code = line.split()[1]
        if stock==code:
            #print("Find the stock in the blacklist: " + stock)
            return True

    #print("Can't find stock in the blacklist")
    return False


#
# 该函数返回股票代码的当前价格是否高于均线价格（均线天数使用 days 参数传入函数）
#
# input parameters:
#   @str : txt filename, include the stock code's price
#   @days: average days, the value is: 15, 30, 60, etc
#
# return value:
#   if current price bigger than the average, return 1, or will return 0
#
# sample:
#   ret = get_turnover_average_result("09923.txt", 5)
#
def get_turnover_average_result(str, days, hasturnover):
    if hasturnover==True:
        # get total lines
        total  = len(open(str, 'r').readlines())

        # get line number(get the line which has the data)
        cnt = (total - 5) / 2 + 2
    else:
        # get line number
        cnt = len(open(str, 'r').readlines())

    # get the line from index value
    # print("cnt is: ", cnt)
    # print("days is: ", days)
    good_lines = cnt - 2    
    if good_lines <= days:
        return 0    

    index = cnt - days + 1
    # print("from index: ", index)

    total = 0.0

    while index <= cnt:
        line = get_line_content(str, index)
        #print(line)
        item4 = line.split()[4]
        #print(item4)
        total += float(item4)        
        index += 1

    average = total / days

    # print(average)
    # print(item4)

    if float(item4) >= average:
        return 1
    else:
        return 0

#
# 该函数返回股票代码的当前价格是否为均线的最次 2 价格（均线天数使用 days 参数传入函数）
# 并且交易额要大于 2 亿人民币
#
# input parameters:
#   @str : txt filename, include the stock code's price
#   @days: average days, the value is: 15, 30, 60, etc
#
# return value:
#   if current price biggest, return 1, or will return 0
#
# sample:
#   ret = get_turnover_max_result("09923.txt", 5)
#
def get_turnover_max_result(str, days, hasturnover):
    if hasturnover==True:
        # get total lines
        total  = len(open(str, 'r').readlines())

        # get line number(get the line which has the data)
        cnt = (total - 5) / 2 + 2
    else:
        # get line number
        cnt = len(open(str, 'r').readlines())

    # get the line from index value
    #print("cnt is: ", cnt)
    #print("days is: ", days)
    good_lines = cnt - 2    
    if good_lines <= days:
        return 0        

    index = cnt - days + 1

    # get the last day data
    line = get_line_content(str, cnt)
    lastVal = line.split()[4]

    #print(line)
    #print(lastVal)

    lastMount = line.split()[5]
    lastMoney = float(lastVal) * float(lastMount)

    #print(lastVal)
    #print(lastMount)
    #print(lastMoney)

    if lastMoney < 200000000:
        return 0

    total = 0

    while index <= cnt:
        line = get_line_content(str, index)
        item4 = line.split()[4]
        #print(item4)
        if float(item4) < float(lastVal):
            total += 1

        index += 1

    if total >= (days - 2):
        return 1
    else:
        return 0

#
# 该函数返回股票代码的最新价格
#
# input parameters:
#   @str : txt filename, include the stock code's price
#
# return value:
#   return the last price of the stock
#
# sample:
#   ret = get_max_result("API.txt", 5)
#
def get_last_price(str, hasturnover):
    if hasturnover==True:
        # get total lines
        total  = len(open(str, 'r').readlines())

        # get line number(get the line which has the data)
        cnt = (total - 5) / 2 + 2
    else:
        # get line number
        cnt = len(open(str, 'r').readlines())

    # get the last day close price
    line = get_line_content(str, cnt)
    lastVal = line.split()[4]

    return lastVal

#
# 该函数基于输入的股票代码stock将历史价格列表返回到参数file指定的文件中
#
# input parameters:
#   @code : stock code, is string
#   @file: the price list write to this file
# 
# sample:
#   get_stock_price_list("09923", "new_09923.txt")
#
def get_stock_price_list(stock, file):
    # show all the row and col
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    # open file and store the stock's price list into the file
    price_obj = open(file, mode = 'w',encoding='utf-8')
    stock_agu_daily_hfq_df = ak.stock_zh_a_daily(symbol=stock, start_date="20201003", end_date="20210221", adjust="qfq")
    print(stock_agu_daily_hfq_df, file=price_obj)
    price_obj.close()

#
# 该函数获取所有 A 股的股票列表，当前总共 4180 至
#
# input parameters:
#   @file: the file to store the stock list
#
# sample:
#   get_agu_list("agu.txt")
#
def get_agu_list(file):
    # show all the row and col
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    # open file and store the stock list into the file
    stock_obj = open(file, mode = 'w',encoding='utf-8')
    agu_stock_list = ak.stock_zh_a_spot()
    print(agu_stock_list, file=stock_obj)
    stock_obj.close()

#
# 该函数返回指定的文件中是否包含某个字符串（从第 2 开始，文件的第一行包含了 turnover 字符串）
#
# input parameters:
#   @str : txt filename, include the stock code's price
#
# return value:
#   if current file include "turnover" string, return 1, or will return 0
#
# sample:
#   ret = has_turnover_line("09923.txt")
#
def has_turnover_line(str):
    # get total lines
    total  = len(open(str, 'r').readlines())

    # skip the first line, which has "turnover" string
    index = 2

    while index <= total:
        line = get_line_content(str, index)        

        ret_index = line.find("turnover")
        if ret_index >= 0:
            # find "turnover" string in the file
            return True
        else:
            index += 1

    # can't find "turnover" string in the file
    return False

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
def add_stock_to_description(line, lastPrice, file):
    wBook = xlrd.open_workbook(file)
    totalRow = wBook.sheets()[0].nrows
    
    writeBook = copy(wBook)
    wooksheet = writeBook.get_sheet(0)
    
    s_item0 = line.split()[0]
    s_item1 = line.split()[1]
    s_item2 = line.split()[2]
    s_item3 = line.split()[3]

    # index to the next line, excel index from zero
    wooksheet.write(totalRow, 0, s_item0)
    wooksheet.write(totalRow, 1, s_item1)
    wooksheet.write(totalRow, 2, s_item2)
    wooksheet.write(totalRow, 3, s_item3)
    wooksheet.write(totalRow, 4, lastPrice)

    writeBook.save(file)    

# help information
print("python  agu.py  [have|no]  [windows|linux]")

#
# 当目录 "test" 中如果已经有了价格列表，执行下面的命令可以节省很多时间
# @ python agu.py have linux/windows
# 否则就执行下面的命令：
# @ python agu.py no linux/windows
#
param1 = sys.argv[1]
param2 = sys.argv[2]


# used to count the output
global_index = 0

# Step.1 use get_agu_list("agu_20210208.txt") get the stock list and remove the price information
# Step.2 as the follow

# Step.1
# get_agu_list("agu_20210208.txt")

# Step.2 as the follow
file = open('agu_20210208.txt','r', encoding='UTF-8')

# create excel file
wb = xlwt.Workbook()
# create worksheet
ws = wb.add_sheet('agu')
raw = 0

print('start time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 

while True:
    line = file.readline()

    # 如果到文件的末尾则退出
    if not line:
        break

    # 获取股票代码
    item1 = line.split()[1]

    # 检查该股票代码是否在黑名单中
    bBlackList = checkBlackList(item1, "blacklist.txt")
    if bBlackList==True:
        continue

    if param2 != "windows":        
        price_list = 'test/' + item1 + '.txt'
    else:
        # Windows platform
        price_list = 'test\\' + item1 + '.txt'

    print("number: " + str(global_index) + " : " + price_list)
    global_index += 1

    # print(price_list)

    # 
    # 获取指定股票的价格列表，并将其写入到指定文件中
    # 如果 test 目录中已经有该文件了，就不用在获取了，节省时间，提高效率
    #
    # 如果有原始数据，11s 时间就可以扫面完成了，否则需要 58 分钟的时间
    #
    if param1 != "have":
        bExist = os.path.exists(price_list)
        if bExist==False:
            get_stock_price_list(item1, price_list)

    # 同时满足如下的均线
    bRet = has_turnover_line(price_list)
    ret30 = get_turnover_average_result(price_list, 30, bRet)
    max30 = get_turnover_max_result(price_list, 30, bRet) 

    if ret30 and max30:
        s_item0 = line.split()[0]
        s_item1 = line.split()[1]
        s_item2 = line.split()[2]
        s_item3 = line.split()[3]

        ws.write(raw, 0, s_item0)
        ws.write(raw, 1, s_item1)
        ws.write(raw, 2, s_item2)
        ws.write(raw, 3, s_item3)

        price = get_last_price(price_list, bRet)    
        ws.write(raw, 4, price)

        # check wether this stock has description
        des = get_stock_description(s_item1, "agu_ref.xls")        
        if des!=None:            
            ws.write(raw, 5, des)
            # 将内容写入 excel 文件中
            wb.save('./agu_20210221.xls')

        else: # add the stock in the orig file
            add_stock_to_description(line, price, "agu_ref.xls")        

        raw += 1

        print(item1)

print("write finished")

print('end time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
