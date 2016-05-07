#-*- coding:utf-8 -*-
import requests
from pandas import DataFrame as df
import pandas as pd
import io
import matplotlib.pyplot as plt
import pymysql

reqdate = '20160412'
file_prefix = "marcap_data_"

print ("start...")
# STEP 01: Generate OTP
gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
gen_otp_data = {
    'name':'fileDown',
    'filetype':'csv',
    'url':'MKD/04/0404/04040200/mkd04040200_01',
    'market_gubun':'ALL', # ''ALL':전체, STK': 코스피
    'indx_ind_cd':'1001',  # '': 전체, ''1001':코스피, 1028' :코스피 200
    'sect_tp_cd':'',
    'schdate':reqdate,
    'pagePath':'/contents/MKD/04/0404/04040200/MKD04040200.jsp',
}
    
r = requests.post(gen_otp_url, gen_otp_data)
code = r.content

# STEP 02: download
down_url = 'http://file.krx.co.kr/download.jspx'
down_data = {
    'code': code,
}

r = requests.post(down_url, down_data).content
df = pd.read_csv(io.StringIO(r.decode("utf-8")), thousands=',', dtype={'종목코드':'str'})

df = df[['종목코드', '종목명', '시가총액(백만원)', '시가총액비중(%)', '상장주식수(천주)']]
df.columns = ['code','corp_name','marcap','marcap_pct','amount']

df['market_gubun'] = 'KS'
df.head(10)


con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='finavis', autocommit=True, use_unicode=True)
con.set_charset('utf8')
cur = con.cursor()

sql_insert = "INSERT INTO stock_info VALUES('%s', '%s', %s, %s, %s, '%s')"
for i in range(len(df)):
    sql = sql_insert % (df.ix[i].code, df.ix[i].corp_name, df.ix[i].marcap, df.ix[i].marcap_pct, df.ix[i].amount, df.ix[i].market_gubun)
    cur.execute(sql)

#cur.execute("insert into stock_info values('051910','LG 화학',21637514, 1.72, 66271100, 'KS')")
cur.execute('select * from stock_info')
result = cur.fetchall()
for row in result:
    print (row)

print ("end...")


'''
class KRX_Collector:
    otp_url = ""
    download_url = ""
    date = ""
    data_path = "./data/"
    file_name = ""
    
    def __init__(self, date, path_dir, filename):
        self.date = date
        self.path_dir = path_dir
        self.filename = filename
        
    def getAllStockListByPrice(self, date):
        if(from_date):
            print (from_date)
        else:
            print ("You should put in the from-to date")
            '''