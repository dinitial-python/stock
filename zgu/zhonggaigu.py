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


# get the line content
def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()

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
    #print ("lines numbers: ", cnt)

    # get the line from index value
    #print("cnt is: ", cnt)
    #print("days is: ", days)
    good_lines = cnt - 2    
    if good_lines <= days:
        return 0    

    index = cnt - days + 1
    #print("from index: ", index)

    total = 0.0

    while index <= cnt:
        line = get_line_context(str, index)
        item4 = line.split()[4]
        #print(item4)
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
#   ret = get_average_result("09923.txt", 5)
#
def get_max_result(str, days):
    # get line number
    cnt = len(open(str, 'r').readlines())
    #print ("lines numbers: ", cnt)

    # get the line from index value
    #print("cnt is: ", cnt)
    #print("days is: ", days)
    good_lines = cnt - 2    
    if good_lines <= days:
        return 0    

    index = cnt - days + 1
    #print("from index: ", index)

    line = get_line_context(str, cnt)
    lastVal = line.split()[4]

    total = 0

    while index <= cnt:
        line = get_line_context(str, index)
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
    #stock_hk_daily_hfq_df = ak.stock_hk_daily(symbol="09923", adjust="hfq")
    stock_us_daily_hfq_df = ak.stock_us_daily(symbol=stock, adjust="")
    print(stock_us_daily_hfq_df, file=price_obj)
    price_obj.close()

#
# 该函数获取中概股的股票列表
#
# input parameters:
#   @file: the file to store the stock list
#
# sample:
#   get_zhonggai_stock_list("zhonggaigu.txt")
#
def get_zhonggai_stock_list(file):
    # show all the row and col
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    # open file and store the stock list into the file
    stock_obj = open(file, mode = 'w',encoding='utf-8')
    # hk_stock_list = ak.stock_us_zh_spot()
    hk_stock_list = ak.get_us_stock_name()
    print(hk_stock_list, file=stock_obj)
    stock_obj.close()


# Step.1 use get_hongkong_stock_list("zhonggaigu.txt") get the stock list and remove the price information
# Step.2 as the follow

file = open('zhonggaigu.txt','r', encoding='UTF-8')

# create excel file
wb = xlwt.Workbook()
# create worksheet
ws = wb.add_sheet('zhonggaigu_')
raw = 0

while True:
    line = file.readline()
    if not line:
        break

    # 获取股票代码
    item1 = line.split()[0]
    price_list = 'test/' + item1 + '.txt'
    #price_list = item1 + '.txt'
    # print("price list file name is: ", price_list)

    # 获取指定股票的价格列表，并将其写入到指定文件中

    #print(price_list)

    get_stock_price_list(item1, price_list)

    #print("finish")

    # 同时满足如下的均线
    ret20 = get_average_result(price_list, 20)
    ret60 = get_average_result(price_list, 60)
    ret120 = get_average_result(price_list, 120)

    ret30 = get_average_result(price_list, 30)
    max30 = get_max_result(price_list, 30)

    if ret30 and max30:

    #if ret20 and ret60 and ret120:
    #if ret60:
        s_item0 = line.split()[0]
        s_item1 = line.split()[1]
        s_item2 = line.split()[2]

        ws.write(raw, 0, s_item0)
        ws.write(raw, 1, s_item1)
        ws.write(raw, 2, s_item2)
        raw += 1

        print(item1)

print("write finished")
wb.save('./stock_20210122.xls')


#
# get_zhonggai_stock_list("zhonggaigu.txt")



'''
# Step.1 use get_hongkong_stock_list("hongkong.txt") get the stock list and remove the price information
# Step.2 as the follow

file = open('hongkong.txt','r', encoding='UTF-8')

# create excel file
wb = xlwt.Workbook()
# create worksheet
ws = wb.add_sheet('hongkong')
raw = 0

while True:
    line = file.readline()
    if not line:
        break

    # 获取股票代码
    item1 = line.split()[1]
    price_list = 'test\\' + item1 + '.txt'
    #price_list = item1 + '.txt'
    # print("price list file name is: ", price_list)

    # 获取指定股票的价格列表，并将其写入到指定文件中
    get_stock_price_list(item1, price_list)

    # 同时满足如下的均线
    ret20 = get_average_result(price_list, 20)
    ret60 = get_average_result(price_list, 60)
    ret120 = get_average_result(price_list, 120)

    if ret20 and ret60 and ret120:
        s_item0 = line.split()[0]
        s_item1 = line.split()[1]
        s_item2 = line.split()[2]

        ws.write(raw, 0, s_item0)
        ws.write(raw, 1, s_item1)
        ws.write(raw, 2, s_item2)
        raw += 1

print("write finished")
wb.save('./stock_20210122.xls')
'''

'''
    if ret20 and ret60 and ret120:
        print(line)
'''

#get_average_result("09923.txt", 60)
''' get_average_result test
ret = get_average_result("09923.txt", 5)
if ret:
    print("current price is bigger")
else:
    print("current price is lower")
'''
