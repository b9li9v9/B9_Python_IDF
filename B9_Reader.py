import pandas as pd
import copy
from B9_UserConfig import UserConfig
class Reader:
    def __init__(self, db_path, field_symbol, field_date, start_date, end_date):
        # 数据库路径
        self.db_path = db_path

        # 内存数据库
        self.db = None

        # 全标的目录
        self.db_directory = []
        # 有效标的目录
        self.db_effective_directory = []
        # 无效标的目录
        self.db_Invalid_directory = []

        # 全标的数量
        self.db_directory_quantity = 0
        # 有效标的数量
        self.db_effective_quantity = 0
        # 无效标的数量
        self.db_Invalid_quantity = 0

        # 下面是字段头二次初始化，用于计算。
        self.field_symbol = field_symbol
        self.field_date = field_date

        # 查阅范围
        # 格式例子 '20061231'
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)

    def Read_Database(self):
        """数据库读入内存 生成目录"""
        df = pd.read_csv(self.db_path)

        # 如果下载的 symbol 为 int，这里进行处理，如果不是也无妨。
        df[self.field_symbol] = df[self.field_symbol].apply(lambda x: '{:0>6}'.format(x))

        # 格式化日期字段
        df[self.field_date] = pd.to_datetime(df[self.field_date])

        # 按Symbol字段分组
        self.db = df.groupby(self.field_symbol)

        # 数据库目录
        self.db_directory = list(self.db.groups.keys())
        # 数据库目录数量
        self.db_directory_quantity = len(self.db_directory)

        # 判断数据时间范围
        for sym in self.db_directory:
            # 标的日期列 是否有end日期
            # 改动这句可以包含判断时间头
            if self.end_date in self.db.get_group(sym)[self.field_date].values:
                # 加入有效目录
                self.db_effective_directory.append(sym)
            else:
                # 加入无效目录
                self.db_Invalid_directory.append(sym)

        # 开停盘数量统计
        self.db_effective_quantity = len(self.db_effective_directory)
        self.db_Invalid_quantity = len(self.db_Invalid_directory)

    def Select_target(self, symbol):
        """数据库组内选中标的，按时间排序"""
        # 日期输入格式例子   '19800101'  '20250101'

        # 根据代码选中 深拷贝
        single_target = copy.deepcopy(self.db.get_group(symbol))
        # 设置日期为索引
        single_target.set_index(self.field_date, inplace=True)
        # 指定数据日期范围
        single_target = single_target[(single_target.index >= self.start_date) & (single_target.index <= self.end_date)]
        # 按时间排序
        single_target.sort_values(by=self.field_date, inplace=True)
        return single_target

# EMreadr = Reader(UserConfig.EMDBPath, 'Symbol', '日期', '19800101', '20230314')
# EMreadr.Read_Database()
#
# print(EMreadr.db)  # 库
# print(EMreadr.db_directory)  # 全标的
# print(EMreadr.db_effective_directory)  # 有效标的
# print(EMreadr.db_Invalid_directory)  # 无效标的
# print(EMreadr.db_directory_quantity)  # 全标的数量
# print(EMreadr.db_effective_quantity)  # 有效数量
# print(EMreadr.db_Invalid_quantity)  # 无效数量
# print(EMreadr.Select_target('000001'))  # 选中单标的
