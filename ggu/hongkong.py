#
# Python reference:
# https://www.runoob.com/python/att-string-split.html
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
# get line number
import sys

# get time
import time

def info(info):
    print(str(sys._getframe().f_lineno) + info)

# get the line content
def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()

# 
# 检查字符串（股票代码）是否在 excel 表格中，如果 excel 包含了指定的股票代码，则返回该代码的描述信息
#
def get_stock_description(stock, file):
    # excel读取准备
    wbook = xlrd.open_workbook(file)
    sheet1 = wbook.sheets()[0]

    # 从第一行开始
    nraw = 0

    while True:
        code = sheet1.cell(nraw, 0).value
        #print(code)

        if code=="END":
            break

        if code == stock:
            #print("code == stock")
            return sheet1.cell(nraw, 2).value

        nraw += 1

    #print("code != stock")
    return None

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

        code = line.split()[0]
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
#   ret = get_average_result("09923.txt", 5)
#
def get_average_result(str, days):
    # get line number
    cnt = len(open(str, 'r').readlines())
    
    good_lines = cnt - 2    
    if good_lines <= days:
        return 0    

    index = cnt - days + 1
    #print("from index: ", index)

    total = 0.0

    while index <= cnt:
        line = get_line_context(str, index)
        item4 = line.split()[4]        
        total += float(item4)
        index += 1

    average = total / days

    if float(item4) >= average:
        return 1
    else:
        return 0

#
# 该函数返回股票代码的当前价格是否为均线的最高价格（均线天数使用 days 参数传入函数）
#
# input parameters:
#   @str : txt filename, include the stock code's price
#   @days: average days, the value is: 15, 30, 60, etc
#
# return value:
#   if current price biggest, return 1, or will return 0
#
# sample:
#   ret = get_max_result("API.txt", 5)
#
def get_max_result(file, days):
    # get line number
    cnt = len(open(file, 'r').readlines())

    good_lines = cnt - 2    
    if good_lines <= days:
        return 0

    index = cnt - days + 1        

    # get the last day close price
    line = get_line_context(file, cnt)
    lastVal = line.split()[4]

    # 获取成交量，用于计算成交额。对于美股，成交额需要大于 1 亿元 RMB
    lastMount = line.split()[5]
    lastMoney = float(lastVal) * float(lastMount)

    if lastMoney < 120000000:
        return 0

    total = 0

    while index <= cnt:
        line = get_line_context(file, index)
        item4 = line.split()[4]

        if float(item4) < float(lastVal):
            total += 1

        index += 1

    if total >= (days - 2):
        return 1
    else:
        return 0

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
    stock_hk_daily_hfq_df = ak.stock_hk_daily(symbol=stock, adjust="qfq")
    print(stock_hk_daily_hfq_df, file=price_obj)
    price_obj.close()

#
# 该函数获取在香港上市的股票列表
#
# input parameters:
#   @file: the file to store the stock list
#
# sample:
#   get_hongkong_stock_list("hongkong.txt")
#
def get_hongkong_stock_list(file):
    # show all the row and col
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    # open file and store the stock list into the file
    stock_obj = open(file, mode = 'w',encoding='utf-8')
    hk_stock_list = ak.stock_hk_spot()
    print(hk_stock_list, file=stock_obj)
    stock_obj.close()

# help information
print("python  hongkong.py  [have|no]  [windows|linux]")

#
# 当目录 "test" 中如果已经有了价格列表，执行下面的命令可以节省很多时间
# @ python hongkong.py have
# 否则就执行下面的命令：
# @ python hongkong.py no
#
param1 = sys.argv[1]
param2 = sys.argv[2]

# Step.1 get hongkong.txt from futu gonggu page
# Step.2 as the follow

file = open('hongkong.txt','r', encoding='UTF-8')

# create excel file
wb = xlwt.Workbook()
# create worksheet
ws = wb.add_sheet('hongkong')
raw = 0

print('start time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

while True:
    line = file.readline()
    if not line:
        break    

    # 获取股票代码
    item1 = line.split()[0]

    # 检查该股票代码是否在黑名单中
    bBlackList = checkBlackList(item1, "blacklist.txt")
    if bBlackList==True:
        continue

    if param2 != "windows":
        price_list = 'test/' + item1 + '.txt'
    else:
		# Windows platform
        price_list = 'test\\' + item1 + '.txt'       
    # print(price_list)

    # 
    # 获取指定股票的价格列表，并将其写入到指定文件中
    # 如果 test 目录中已经有该文件了，就不用在获取了，节省时间，提高效率

    # 如果有原始数据，11s 时间就可以扫面完成了，否则需要 30 分钟到 2 小时的时间
    #
    if param1 != "have":
        get_stock_price_list(item1, price_list)

    # 同时满足如下的均线条件
    ret30 = get_average_result(price_list, 30)
    max30 = get_max_result(price_list, 30)

    if ret30 and max30:
        s_item0 = line.split()[0]
        s_item1 = line.split()[1]
        #s_item2 = line.split()[2]

        ws.write(raw, 0, s_item0)
        ws.write(raw, 1, s_item1)

        # 返回股票的描述信息
        des = get_stock_description(s_item0, "ggu_20210211.old.xls")
        if des!=None:
            ws.write(raw, 2, des)

        wb.save('./ggu_20210211.xls')

        raw += 1

        print(item1)

print("write finished")

print('end time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
