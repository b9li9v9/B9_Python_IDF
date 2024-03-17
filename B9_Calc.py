import pandas as pd
import ta
class Calc:

    # 转换K线周期
    @classmethod
    def Quotes_Convert_K_line(cls,cycle,target,field_symbol,field_open,field_close,field_high,field_low,field_vol,field_TO,field_Amp,field_PCR,field_PCA,field_tr):
        #  ['股票代码','日期','开盘','收盘','最高','最低','成交量','成交额','振幅','涨跌幅','涨跌额','换手率']
        #  ['Symbol','Date','Open','Close','High','Low','Vol','TO',"Amp", "PCR", "PCA", "TR"]

        single = target.copy()
        # 添加OS字段 流通股本 这里是倒推约算所以有细微误差，因为数据源没给流通股本。
        single['流通股本(约)'] = (target[field_vol] / target[field_tr]) * 10000

        # 测试轮
        single_converter = single.resample(cycle).agg(
            {field_open: 'first', field_high: 'max', field_low: 'min', field_close: 'last',
             field_vol: 'sum', field_TO: 'sum', '流通股本(约)': 'mean'})
        single_converter[field_Amp] = ((single_converter[field_high] - single_converter[field_low]) /
                                   single_converter[field_close].shift(1).ffill()) * 100
        single_converter[field_PCR] = ((single_converter[field_close] - single_converter[field_close].shift(
            1)).fillna(0) / single_converter[field_close].shift(1).ffill()) * 100
        single_converter[field_PCA] = single_converter[field_close] - single_converter[field_close].shift(1)
        single_converter[field_tr] = (single_converter[field_vol] / single_converter['流通股本(约)']) * 10000

        # 这要加个股票代码字段
        single_converter[field_symbol] = single[field_symbol].iat[0]
        return single_converter

    # 生成标的MACD
    @classmethod
    def Quotes_Macd(cls,df,field_close):
        df['Macd'] = ta.trend.macd_diff(df[field_close]) * 2
        return df

