介绍:

    投资数据过滤器 Investment Data Filter
    整体上这些代码没什么用，写给自己用的
    
    
使用:
    
    Reader.py 读取器 
    Test.py 测试
    
整体思路:
    
    Reader读取有代码和日期字段的数据库
    按代码进行分组、再按时间范围切片排序
    整理后可以.Select_target选中单标的进行后续的计算 
工具:

    win10 AMD64
    python 3.8.10 AMD64
    
    akshare==1.12.31
    pandas==2.0.3
    ta==0.11.0
    TA-Lib==0.4.24
