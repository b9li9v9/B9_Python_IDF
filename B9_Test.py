from B9_Reader import Reader
from B9_Calc import Calc
from B9_UserConfig import UserConfig

EMreadr = Reader(UserConfig.EMDBPath, 'Symbol', '日期', '19800101', '20250101')
EMreadr.Read_Database()

print(EMreadr.db)  # 库
print(EMreadr.db_directory)  # 全标的

for single in EMreadr.db_directory:
    SG = EMreadr.Select_target(single)
    # 单标的转换K线后 SGCK
    SGCK = Calc.Quotes_Convert_K_line('W',SG,'Symbol','开盘','收盘','最高','最低','成交量','成交额','振幅','涨跌幅','涨跌额','换手率')
    print(SGCK)
    # 生成MACD
    SGCKM = Calc.Quotes_Macd(SGCK,'收盘')
    print(SGCKM)
