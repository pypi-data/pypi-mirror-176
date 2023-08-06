import chinese_calendar
import datetime
import pandas as pd
import baostock as bs
import tushare as ts
import requests

def get_tradeday(start_str,end_str):
    start = datetime.datetime.strptime(start_str, '%Y-%m-%d') # 将字符串转换为datetime格式
    end = datetime.datetime.strptime(end_str, '%Y-%m-%d')
    # 获取指定范围内工作日列表
    lst = chinese_calendar.get_workdays(start,end)
    expt = []

    # 找出列表中的周六，周日，并添加到空列表
    for time in lst:
        if time.isoweekday() == 6 or time.isoweekday() == 7:
            expt.append(time)
    # 将周六周日排除出交易日列表
    for time in expt:
        lst.remove(time)
    date_list = [item.strftime('%Y-%m-%d') for item in lst] #列表生成式，strftime为转换日期格式
    return date_list

def getdatafrombaostock(stnamelist,stday,edday,fq,otpath,is_f,add_or_rpl): #stday,edday like 'xxxx-xx-xx'  #otpath 以 \\ 结尾

    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    name_list = pd.read_csv(stnamelist)
    L = len(name_list)
    j = 0
    while(j < L):

        stock_code = name_list.ts_code[j]

        rs = bs.query_history_k_data_plus(stock_code,
            "date,time,code,open,high,low,close,volume,amount,adjustflag",
            start_date = stday, end_date = edday,
            frequency = fq , adjustflag = "3")

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        
        if(is_f == 'f'):
            #### 结果集输出到csv文件 ####   
            if(add_or_rpl == 'add'):
             result.to_csv(otpath + stock_code +'.csv', header=None ,index=False,mode='a')
            else:
             result.to_csv(otpath + stock_code +'.csv', index=False)
        else :
            return result

        print(j+1)

        j += 1


    bs.logout()

def get_alldatebar(tk,st,ed,is_f,otpath):#起止日期 like xxxx-xx-xx #otpath 以 \\ 结尾

    pre_path = otpath

    lst = get_tradeday(st,ed)

    i = 0
    while(i < len(lst)):
        s = lst[i]
        lst[i] = s[0]+s[1]+s[2]+s[3]+s[5]+s[6]+s[8]+s[9]
        i += 1


    #44bd527b59125d78c4cb094bd152e6e86bd7ed0fb8056c678439b764

    ts.set_token(tk)

    pro = ts.pro_api()

    j = 0

    while(j<len(lst)):
        
        df = pro.daily(trade_date=lst[j])

        ticks_df = pd.DataFrame(df)

        if(is_f == 'f'):

          ticks_df.to_csv(pre_path + 'T' + lst[j] + '.csv', index=0)

        else :
          return ticks_df

        j += 1
        print("fininsh" + str(j))


def get_alldatebar_singleday(tk,date,is_f,otpath):#起止日期 like xxxx-xx-xx #otpath 以 \\ 结尾

    pre_path = otpath

    #44bd527b59125d78c4cb094bd152e6e86bd7ed0fb8056c678439b764

    ts.set_token(tk)

    pro = ts.pro_api()

        
    df = pro.daily(trade_date=date)

    ticks_df = pd.DataFrame(df)

    if(is_f == 'f'):

        ticks_df.to_csv(pre_path + 'T' + date + '.csv', index=0)

    else :
        return ticks_df

    print("fininsh")

def get_tick(stock_code) :
      headers = {'referer': 'http://finance.sina.com.cn'}
      resp = requests.get('http://hq.sinajs.cn/list=' + 'sh' + stock_code, headers=headers, timeout=6)
      data = resp.text
      list1 = data.split(',')
      #{
      # 0 名称
      # 1 今开
      # 2 昨收
      # 3 此时价格
      # 4 最高
      # 5 最低
      # 30 年月天
      # 31 时分秒
      # }
      #last = list1[3]
      #trade_datetime = list1[30] + ' ' + list1[31]
      #self.tick = (trade_datetime,last)
      return list1

def get_history_bill(stock_code: str) -> pd.DataFrame:
    '''
    获取多日单子数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）

    '''
    EastmoneyHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入',
        'f57': '主力净流入占比',
        'f58': '小单流入净占比',
        'f59': '中单流入净占比',
        'f60': '大单流入净占比',
        'f61': '超大单流入净占比',
        'f62': '收盘价',
        'f63': '涨跌幅'
    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    for i in range(0,1):
        # 沪市指数
        if stock_code[:3] == '000':
            stock_code = f'0.{stock_code}'
            break
        # 深证指数
        if stock_code[:3] == '399':
            stock_code = f'0.{stock_code}'
            break
        # 沪市股票
        if stock_code[0] != '6':
            stock_code = f'0.{stock_code}'
            break
        # 深市股票
        stock_code = f'1.{stock_code}'
        break

    secid = stock_code
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),

    )
    params = dict(params)
    url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
    json_response = requests.get(url,
                                 headers=EastmoneyHeaders, params=params).json()
    data = json_response.get('data')
    
    if data is None:
        if secid[0] == '0':
            secid = f'1.{stock_code}'
        else:
            secid = f'0.{stock_code}'
        params['secid'] = secid
        
        json_response: dict = requests.get(url, headers=EastmoneyHeaders,params=params).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', stock_code, '可能有误')
        return pd.DataFrame(columns=columns)
    if json_response is None:
        return
    data = json_response['data']
    klines = data['klines']
    rows = []
    for _kline in klines:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df


