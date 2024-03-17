import akshare as ak
import time
import pandas as pd

from B9_Logger import Logger
from B9_UserConfig import UserConfig

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# 东财接口
class EM:
    # 股票目录
    StockDir = None

    @classmethod
    # Symbol,日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
    def InitCsvFile(cls,field_head,DB_file_name):
        fh = field_head
        with open(DB_file_name, 'w', encoding='UTF-8') as file:
            file.write(fh)

    @classmethod
    def GetStockDir(cls):
        """创建股票目录，转储为list"""
        # 使用 akshare 库获取全市场的股票名单
        stock_list = ak.stock_zh_a_spot_em()
        cls.StockDir = stock_list['代码'].tolist()

    @classmethod
    # 行情级别需查akshareAPI
    def AddQuotes(cls,speed,Symbol,DB_file_name,adj,Period,Start_date,End_date,field_Symbol=None):
        """创建及补充行情"""
        # 存入的数据不包含字段头
        # 数据范围含时间头、尾
        # 例子 0.1,'000001',Write_EM_dB_path,'qfq','daily','20240128','20240129','Symbol'
        # field_Symbol参数用于没有symbol字段的数据源 会以实参字符串构建字段头
        try:
            daily = ak.stock_zh_a_hist(symbol=Symbol, period=Period, start_date=Start_date, end_date=End_date, adjust=adj)
            if field_Symbol != None:
                daily.insert(0, field_Symbol, Symbol)
            daily.to_csv(DB_file_name, mode='a',index=False, header=False)
            time.sleep(speed)
        except:
            message = f"EM_Build {Symbol} 爬取失败\n"
            Logger.write_log(message)

# 初始DB字段头
# fh = 'Symbol,日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率\n'
# EM.InitCsvFile(fh,UserConfig.EMDBPath)

# 获取全市场标的目录
# EM.GetStockDir()

# 打印目录
# print(EM.StockDir)

# 单标的写入
# EM.AddQuotes(0.1,'000001',UserConfig.EMDBPath,'qfq','daily','20230101','20240129','Symbol')

# 全市场写入
# total = len(EM.StockDir)
# ind = 1
# for i in EM.StockDir:
#     EM.AddQuotes(1,i,UserConfig.EMDBPath,'qfq','daily','19800101','20240223','Symbol')
#     print(total,ind,i)
#     ind += 1





# 同花顺接口 财务数据
class THS:
    FinanceDir = None

    # 股票代码,报告期,净利润,净利润同比增长率,扣非净利润,扣非净利润同比增长率,营业总收入,营业总收入同比增长率,基本每股收益,每股净资产,每股资本公积金,每股未分配利润,每股经营现金流,销售净利率,销售毛利率,净资产收益率,净资产收益率-摊薄,营业周期,存货周转率,存货周转天数,应收账款周转天数,流动比率,速动比率,保守速动比率,产权比率,资产负债率
    @classmethod
    def InitCsvFile(cls, field_head, DB_file_name):
        fh = field_head
        with open(DB_file_name, 'w', encoding='UTF-8') as file:
            file.write(fh)


    @classmethod
    def GetFinanceDir(cls):
        pass

    @classmethod
    def AddFinance(cls,path,symbol,Period,field_Symbol):
        # 单季度 财报
        # 参数例子 Write_THS_db_path,'000001',"按单季度",'股票代码'

        # 获取数据
        stock_financial_abstract_ths_df = ak.stock_financial_abstract_ths(symbol=symbol, indicator=Period)
        # 初始字段头格式
        stock_financial_abstract_ths_df.insert(loc=0, column=field_Symbol, value=symbol)
        # 写入文件 关闭字段头
        stock_financial_abstract_ths_df.to_csv(path, sep=",", mode='a', encoding="utf-8",index=False,header=False)

# thsfh = '股票代码,报告期,净利润,净利润同比增长率,扣非净利润,扣非净利润同比增长率,营业总收入,营业总收入同比增长率,基本每股收益,每股净资产,每股资本公积金,每股未分配利润,每股经营现金流,销售净利率,销售毛利率,净资产收益率,净资产收益率-摊薄,营业周期,存货周转率,存货周转天数,应收账款周转天数,流动比率,速动比率,保守速动比率,产权比率,资产负债率\n'
# THS.InitCsvFile(thsfh,UserConfig.THSDBPath)
# THS.AddFinance(UserConfig.THSDBPath,'000001',"按单季度",'股票代码')
