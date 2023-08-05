import datetime as dt
import time


# 获得当前股票的最新价格，获得当前的价格，和周期相关，默认周期是日线，获得的是日线级别数据，默认的是分钟，获得的是分钟级别的数据
# 9点30分在回测时，一分钟数据不能获得，在9点31分的时候，可用获得1分钟数据
def get_current_data(ContextInfo, stock):
    current_time = get_current_time(ContextInfo)
    data = ContextInfo.get_market_data_ex(fields=['open', 'close', 'high', 'low'], stock_code=[stock], period='follow',
                                          end_time=current_time, count=1,
                                          dividend_type='follow', fill_data=True, subscribe=True)
    print("data   %s", data)
    # print("current_data[stock]['close'].values[0]   %s",data[stock]['close'].values[0])
    return data[stock]


# 获得当前时间
def timetag_to_datetime(realtimetag, YmdHMS):
    realtimetag = time.localtime(realtimetag)
    return time.strftime( YmdHMS,realtimetag)


def get_current_time(ContextInfo):
    # 日线级别运行第一个时间是 00:00:00
    index = ContextInfo.barpos
    realtimetag = ContextInfo.get_bar_timetag(index)
    current_time = timetag_to_datetime(realtimetag, ContextInfo.YmdHMS)
    print(timetag_to_datetime(realtimetag, '%Y%m%d %H:%M:%S'))
    if current_time == '19700101080000':
        return dt.datetime.now().strftime(ContextInfo.YmdHMS)
    return timetag_to_datetime(realtimetag, ContextInfo.YmdHMS)


def test_time_tag_to_datetime():
    time_str = timetag_to_datetime(1667800769, '%Y-%m-%d %H:%M:%S')
    assert time_str == '2022-11-07 13:59:29',"time_str "+time_str


def test():
    test_time_tag_to_datetime()

