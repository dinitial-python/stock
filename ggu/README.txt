1.备注
  1）使用同花顺，选择港股，数据导出，导出所有数据，选择导出到剪贴板。
  2）新建文本文件，使用 notepad++ 打开，将剪贴板中的内容黏贴到该文本文件中

去掉：
04604		ICBC EURPREF1	
04607		CINDA 16USDPREF	
04609		CMBC 16USDPREF	
04610		CZB 17USDPREF	
04611		BQD 17USDPREF	
04612		PSBC 17USDPREF	
04613		ZZBNK 17USDPREF	
04614		CMB 17USDPREF	
04615		BOJZ 17USDPREF	
04616		BCQ 17USDPREF	
01473		环联连讯
04608		HSBNK 16USDPREF	
04617		ZYBNK 18USDPREF	
04618		GRCB 19USDPREF	
04619		BOC 20USDPREF	
04620		ICBC 20USDPREF	
06606		诺辉健康-B	
06688		蚂蚁集团	
08302		STOCK8302	
08303		STOCK8303	
08304		STOCK8304
01015		STOCK1015	
01016		STOCK1016	
01017		STOCK1017	
01018		STOCK1018

3）注意：
  需要在文件 “ggu_20210211.old.xls”的最后一行手动增加 "END" 字符串，用来标记 excel 文件的结尾。

4）修改（重要，注意）
  A.如果有原始数据，11s 时间就可以扫面完成了，否则需要 30 分钟到 2 小时的时间 。如果没有原始数据就需要将函数“get_stock_price_list”调用的注释打开
  B.在拷贝“ggu_20210211.old.xls”中数据描述的时候，需要在文件 “ggu_20210211.old.xls”的最后一行手动增加 "END" 字符串，用来标记 excel 文件的结尾。

5）执行命令
  A.当 "test" 目录下包含了输出的股票的价格列表时，执行下面的命令就不用在生成了，时间只需要 11 秒左右。
  (ak_test) C:\Users\daniel.dong\Documents\GitHub\stock\ggu>python hongkong.py have

  B.如果需要在 test 目录下重新生成股票的价格列表，执行下面的命令，会消耗较多的时间，以小时为单位：
  (ak_test) C:\Users\daniel.dong\Documents\GitHub\stock\ggu>python hongkong.py no


2.更新时间
1）第 1 次
C:\Users\daniel.dong>date
当前日期: 2021/02/11 周四
输入新日期: (年月日)