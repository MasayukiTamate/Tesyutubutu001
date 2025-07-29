from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib import pyplot as pl
import streamlit as st
import numpy as np
import yfinance as yf
import datetime

text_name2 = "c:/Users/manaby/Documents/python/stock_price.txt"
data_j_name2 = "c:/Users/manaby/Documents/python/data_j.xls"
text_name = "stock_price.txt"
data_j_name = "data_j.xls"
text_name2  = "c:/Users/横浜関内駅前事業所/Documents/python/stock_price.txt"
data_j_name2 = "C:/Users/横浜関内駅前事業所/Documents/python/data_j.xls"
with open(text_name2,"r") as f:
        stock_file_data = f.read()

data_j = pd.read_excel(data_j_name2,sheet_name=0, index_col=0)

stock_file_data = stock_file_data.split()
stock_data = []
for stock_string in stock_file_data:
        stock_data.append(float(stock_string))

#print("株価",stock_data)
n_price = len(stock_data)
#print("データ数",n_price)

ratio_data = []
for i in range(1, n_price):
    ratio_data.append(float(stock_data[i] - stock_data[i - 1]) / float(stock_data[i - 1]))

n_ratio = len(ratio_data)
#print("変化率",ratio_data)

successive_data = []
answers = []
for i in range(4,n_ratio):
    successive_data.append([ratio_data[i-4], ratio_data[i-3],ratio_data[i-2],ratio_data[i-1]])
    if ratio_data[i] > 0:
        answers.append(1)
    else:
        answers.append(0)
#print("4日連続の変化率", successive_data)
#print("正解", answers)

x_train, x_test, t_train, t_test = train_test_split(successive_data, answers, shuffle=False)

clf = svm.SVC()
clf.fit(x_train, t_train)

y_test = clf.predict(x_test)

a = -20
b = a + 10

#print("正解", t_test[a:b])
#print("予測", y_test[a:b])

correct = 0.0
wrong = 0.0
for i in range(len(t_test)):
    if y_test[i] == t_test[i]:
        correct += 1.0
    else:
        wrong += 1.0

#print("正解率", str(correct / (correct + wrong) * 100), "％")




data_j = data_j[["コード","銘柄名"]]#銘柄エクセルファイルを辞書型にする
#Stock_name = st.text_input("銘柄：")
list_meigara = data_j["銘柄名"].unique()#銘柄リスト

kouho_name = st.selectbox("銘柄：",list_meigara)#株価を見たい銘柄インプット

meigara_code_list = data_j["コード"].unique()#銘柄コードリスト


Stock_Code = ""
kazu = 0
flag = True

#銘柄からコードを摘出※要修正
while flag:
    if kouho_name == "":
         flag = False
    if kouho_name == str(list_meigara[kazu]):
          Stock_Code = meigara_code_list[kazu]
          flag = False
    if kazu+1 >= len(meigara_code_list):
         flag = False
    else:
        kazu = kazu + 1

now_date = datetime.date(2025,4,30)
max_date = now_date
start_date = st.date_input("この日から表示：",now_date)
end_date = st.date_input("この日まで表示：",now_date)
#start_date =  end_date + datetime.timedelta(days=-10)

     

Stock_Code = str(Stock_Code) + ".T"


stockstock = yf.Ticker(Stock_Code)
#株価表示
if st.checkbox(""):
    STOCK_download = yf.download(Stock_Code,end=end_date,start=start_date)
    df = pd.DataFrame(STOCK_download)

    st.dataframe(df.style.highlight_max(axis=0))
st.write(Stock_Code)