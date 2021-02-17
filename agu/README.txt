


[Q1.（21:51 2021/2/17）]
1.文件描述
  1）agu_old.xls 用于临时保存获取的 A 股股票列表，后面会删除；
  2）agu_ref.xls 参考股票列表，用来保存股票的描述信息，随着时间会逐步累积；
  3）agu_日期.xls 基于该程序执行的日期生成文件
2.更细累计
  随着时间的累积，主要是对 agu_ref.xls 文件进行更新。可以对每只股票增加五角星号，用来表示股票的关注程度




[时间旧]


1.备注
  1）A 股的数据通过 akshare 接口获取的，数据比较全。获取数据后去掉如下首行：
       symbol    code    name    trade  pricechange  changepercent      buy  \

  2）执行命令如下：
      (ak_test) C:\Users\daniel.dong\Documents\GitHub\stock\agu>python agu.py have/no windows/linux

  例如，在 Windows 平台下，当”test“目录下存放了股票的价格列表的时候，执行如下命令：
      (ak_test) C:\Users\daniel.dong\Documents\GitHub\stock\agu>python agu.py have windows

 3）目前打印出来的股票的列表是成交额大于 2 亿元人民币。中概股的成交额是大于 5000 万（3 亿人民币）美金，因为美股可以当冲，成交额要求会大一些。

2.保存
把每天扫描出来的股票列表基于日期保存到文件中，提交的 git 仓库，作为历史记录的数据保存。（例如保存文件 agu_20210212.old.xls）
