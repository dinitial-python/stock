#
# get American market stock list for research
#
# support: excel read and write; get local time for count
#
import pandas as pd
import akshare as ak
import linecache
import xlwt
import xlrd
import sys
import time
import os

#
# debug function
#
def info(info):
    print(str(sys._getframe().f_lineno) + info)

#
# get content of a line
#
def get_line_content(file_path, line_number):
    return linecache.getline(file_path, int(line_number)).strip()

#
# check wether the stock is in the blacklist file
#
def checkBlackList(stock, filename):
    file = open(filename,'r', encoding='UTF-8')

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
# Get last price of the stock
#
def get_last_price(pricelist):
    # get line number
    cnt = len(open(pricelist, 'r').readlines())

    # get the last day close price
    lastLine = get_line_content(pricelist, cnt)
    lastPrice = lastLine.split()[4]

    return lastPrice

#
# check wether current stock price is bigger than the average of the days
#
def bigger_than_average(pricelist, days):
    # get line number
    cnt = len(open(pricelist, 'r').readlines())
    
    good_lines = cnt - 2
    if good_lines <= days:
        return False

    # from the index
    index = cnt - days + 1

    total = 0.0

    while index <= cnt:
        line = get_line_content(pricelist, index)
        item4 = line.split()[4]        
        total += float(item4)
        index += 1

    average = total / days

    if float(item4) >= average:
        return True
    else:
        return False

#
# check wether current stock price is lower than the average of the days
#
def lower_than_average(pricelist, days):
    # get line number
    cnt = len(open(pricelist, 'r').readlines())
    
    good_lines = cnt - 2
    if good_lines <= days:
        return False

    # from the index
    index = cnt - days + 1

    total = 0.0

    while index <= cnt:
        line = get_line_content(pricelist, index)
        item4 = line.split()[4]        
        total += float(item4)
        index += 1

    average = total / days

    if float(item4) < average:
        return True
    else:
        return False

#
# check wether current stock price is bigger than the specific number of days
# Current the day is total days - 2
#
def bigger_than_total(pricelist, days):
    # get line number
    cnt = len(open(pricelist, 'r').readlines())

    good_lines = cnt - 2    
    if good_lines <= days:
        return 0

    index = cnt - days + 1

    # get the last day close price
    lastLine = get_line_content(pricelist, cnt)
    lastPrice = lastLine.split()[4]

    # the last sell money must bigger than 50000000 dollar
    lastMount = lastLine.split()[5]
    lastMoney = float(lastPrice) * float(lastMount)    
    if lastMoney < 50000000:
        return False

    totalDay = 0

    while index <= cnt:
        line = get_line_content(pricelist, index)
        item4 = line.split()[4]

        if float(item4) < float(lastPrice):
            totalDay += 1

        index += 1

    if totalDay >= (days - 2):
        return True
    else:
        return False

#
# check wether current stock price is lower than the specific number of days
# Current the day is total days - 2
#
def lower_than_total(pricelist, days):
    # get line number
    cnt = len(open(pricelist, 'r').readlines())

    good_lines = cnt - 2    
    if good_lines <= days:
        return 0

    index = cnt - days + 1

    # get the last day close price
    lastLine = get_line_content(pricelist, cnt)
    lastPrice = lastLine.split()[4]

    # the last sell money must bigger than 50000000 dollar
    lastMount = lastLine.split()[5]
    lastMoney = float(lastPrice) * float(lastMount)    
    if lastMoney < 50000000:
        return False

    totalDay = 0

    while index <= cnt:
        line = get_line_content(pricelist, index)
        item4 = line.split()[4]

        if float(lastPrice) < float(item4):
            totalDay += 1

        index += 1

    if totalDay >= (days - 2):
        return True
    else:
        return False

#
# store the stock's price list in the file
#
def get_stock_price_list(stock, filename):    
    # show all the row and col
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)

    # open file and store the stock's price list in this file
    price_obj = open(filename, mode = 'w',encoding='utf-8')
    daily_us_qfq = ak.stock_us_daily(symbol=stock, adjust="qfq")
    print(daily_us_qfq, file=price_obj)
    price_obj.close()

#
# Up trend following
#
def up_trend_following(listPrice, days):
    # get the result
    avg30 = bigger_than_average(listPrice, days)
    tot30 = bigger_than_total(listPrice, days)

    if avg30 and tot30:
        return True
    else:
        return False

#
# Down trend following
#
def down_trend_following(listPrice, days):
    # get the result
    avg30 = lower_than_average(listPrice, days)
    tot30 = lower_than_total(listPrice, days)

    if avg30 and tot30:
        return True
    else:
        return False


# help information
print("python  mgu.py  [windows|linux]  [up|down]  [have|no]")

#
# python mgu.py [platform] [trend] [test] 
# @platform: windows | linux
# @trend: up | down
# @test: have | no
#
param1 = sys.argv[1]
param2 = sys.argv[2]
param3 = sys.argv[3]

# open excel file and create the sheet
wBook = xlwt.Workbook()
wSheet = wBook.add_sheet('mgu')

# index the raw of excel file
raw = 0

# used to count the output
global_index = 0

# open stock list file
stockList = open('20210212_mgu.txt','r', encoding='UTF-8')

# star to count time
print('start time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

while True:
    line = stockList.readline()
    if not line:
        break    
    
    # get the stock name from stock list file
    item1 = line.split()[1]

    # check wether the this stock is in the blacklist
    bBlackList = checkBlackList(item1, "blacklist.txt")
    if bBlackList==True:
        continue

    if param1 != "windows":
        price_list = 'test/' + item1 + '.txt'
    else:
        # Windows platform
        price_list = 'test\\' + item1 + '.txt'
    
    print("number: " + str(global_index) + " : " + price_list)
    global_index += 1

    if param3 != "have":        
        #bExist = os.path.exists(price_list)
        #if bExist==False:
        get_stock_price_list(item1, price_list)
    
    if param2 == "down":
        trend = down_trend_following(price_list, 7)
    else:
        trend = up_trend_following(price_list, 30)

    if trend==True:
        s_item0 = line.split()[0]
        s_item1 = line.split()[1]
        s_item2 = line.split()[2]

        wSheet.write(raw, 0, s_item0)
        wSheet.write(raw, 1, s_item1)
        wSheet.write(raw, 2, s_item2)

        # append last price of the stock
        price = get_last_price(price_list)
        wSheet.write(raw, 3, price)

        # write the result to excel file
        if param2 == "down":
            wBook.save('./mgu_20210217_down.xls')
        else:
            wBook.save('./mgu_20210217_up.xls')

        raw += 1

        print(item1)    

print("write finished")

# end to count time
print('end time: %s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 