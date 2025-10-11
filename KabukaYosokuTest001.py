from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib import pyplot as pl
import streamlit as st
import numpy as np
import yfinance as yf
import datetime
import time

#フォルダ名文字列
text_name2  = "c:/Users/横浜関内駅前事業所/Documents/python/" + "stock_price.txt"
data_j_name2 = "C:/Users/横浜関内駅前事業所/Documents/python/" + "data_j.xls"
text_name2 = "stock_price.txt"
data_j_name2 = "data_j.xls"

#エクセルとテキストのデータを読み込む
with open(text_name2,"r") as f:
        stock_file_data = f.read()

data_j = pd.read_excel(data_j_name2,sheet_name=0, index_col=0)

stock_file_data = stock_file_data.split()

stock_data = []
for stock_string in stock_file_data:
        stock_data.append(float(stock_string))


n_price = len(stock_data)


ratio_data = []
for i in range(1, n_price):
    ratio_data.append(float(stock_data[i] - stock_data[i - 1]) / float(stock_data[i - 1]))

n_ratio = len(ratio_data)


successive_data = []
answers = []
for i in range(4,n_ratio):
    successive_data.append([ratio_data[i-4], ratio_data[i-3],ratio_data[i-2],ratio_data[i-1]])
    if ratio_data[i] > 0:
        answers.append(1)
    else:
        answers.append(0)


x_train, x_test, t_train, t_test = train_test_split(successive_data, answers, shuffle=False)

clf = svm.SVC()
clf.fit(x_train, t_train)

y_test = clf.predict(x_test)

a = -20
b = a + 10



correct = 0.0
wrong = 0.0
for i in range(len(t_test)):
    if y_test[i] == t_test[i]:
        correct += 1.0
    else:
        wrong += 1.0


st.title = "株価表示～日付指定～"
st.header("株価表示～日付指定～")


#銘柄名からこ銘柄コードを代入する為の前準備
data_j = data_j[["コード","銘柄名"]]#銘柄エクセルファイルを辞書型にする
list_meigara = data_j["銘柄名"].unique()#銘柄リスト
kouho_name = st.selectbox("銘柄：",list_meigara)#株価を見たい銘柄インプット
meigara_code_list = data_j["コード"].unique()#銘柄コードのリスト


#銘柄からコードを摘出※要修正
Stock_Code = ""
kazu = 0
flag = True

while flag:#ループ※何のループか
    if kouho_name == "":
         flag = False
    if kouho_name == str(list_meigara[kazu]):
          Stock_Code = meigara_code_list[kazu]
          flag = False
    if kazu+1 >= len(meigara_code_list):
         flag = False
    else:
        kazu = kazu + 1

#表示する範囲の日にちインプット
dt_now = datetime.datetime.now()
now_date = datetime.date(dt_now.year,dt_now.month,dt_now.day)

month = dt_now.month
day = dt_now.day - 7
if dt_now.day - 7 < 1 :
    day = 30 + (dt_now.day - 7)
    month = dt_now.month -1
if month < 1:
    month = 12
print(f"{month=} {day=}")
befor = datetime.date(dt_now.year, month, day)
max_date = now_date
start_date = st.date_input("この日から表示：",befor)
end_date = st.date_input("この日まで表示：",now_date)
     
cl = []
cl2 = ['最終','最高','最低','開始','値']
Stock_Code = str(Stock_Code) + ".T"
stockstock = yf.Ticker(Stock_Code)
#株価表示
data = []

ckBox = st.checkbox("",value= True,key = 1)

if ckBox:
    STOCK_download = yf.download(Stock_Code,end=end_date,start=start_date)
    df = pd.DataFrame(STOCK_download)


#列名を変更して元に戻す
#関数化予定
    for i in df.columns:
         n = True
         for j in i:
            if n:
                cl.append(j)
                n = False
            else:
                n = True
            
    m = 0

    for i,j in zip(cl,cl2):
        df.rename(columns={i:j},inplace=True)
         

#データフレームを表示
    st.dataframe(df.style.format("{:.2f}"))
#    st.dataframe()
    
    m = 0
    for i in df.columns:
        n = True
         
        for j in i:
            if n:
                i = cl[m]
                n = False
            else:
                n = True
        m = m + 1
#関数化～予定

