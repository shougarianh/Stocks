from data import data
from pandas import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# get the data from the excel file
df = pd.read_excel('companyData.xlsx')
# Change the data frame to be indexed by date
df = df.set_index(pd.DatetimeIndex(df['date'].values))
# make a graph
plt.figure(figsize=(14.0,8.0))
plt.plot(df['4. close'], label='close')
plt.title('Daily close price')
plt.xticks(rotation = 45)
plt.xlabel('Date')
plt.ylabel('Price $')
# plt.show()

# Calculate MACD and signal line indicators
# Calculate the short term exponential moving average (EMA)
short_EMA = df['4. close'].ewm(span=12, adjust = False).mean()
# Calculate long term exponential moving average
long_EMA = df['4. close'].ewm(span=26, adjust = False).mean()
# calculate MACD line
MACD = short_EMA - long_EMA
# create signal line
signal = MACD.ewm(span=9, adjust= False).mean()
plt.figure(figsize=(12.5, 5.0))
plt.plot(df.index, MACD, label = 'DAL MACD', color='red')
plt.plot(df.index, signal, label = 'Signal line', color='blue')
plt.legend(loc='upper left')
plt.show()

# create new columns for data
df['MACD'] = MACD
df['Signal'] = signal

# create function to buy or sell
def buy_sell(signal):
    buy = []
    sell = []
    flag = -1
    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal'][i]:
            sell.append(np.nan)
            if flag != 1:
                buy.append((signal['4. close'][i]))
                flag = 1
            else:
                buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal'][i]:
            buy.append(np.nan)
            if flag != 0:
                sell.append((signal['4. close'][i]))
                flag = 0
            else:
                sell.append(np.nan)
        else:
            sell.append(np.nan)
            buy.append(np.nan)
    return (buy, sell)
# print(short_EMA)
# print(df)
a = buy_sell(df)
df['Buy_Signal_Price'] = a[0]
df['Sell_Signal_Price'] = a[1]
#show the data
plt.figure(figsize=(12.5, 4.5))
plt.scatter(df.index, df['Buy_Signal_Price'], color='green', label='Buy', marker='^', alpha=1)
plt.scatter(df.index, df['Sell_Signal_Price'], color='red', label='Sell', marker='v', alpha=1)
plt.plot(df.index, df['4. close'], label='Close Price', alpha = 0.35)
plt.title('Close price buy/sell signals')
plt.xlabel('Date')
plt.ylabel('Close price $')
plt.legend(loc = 'upper left')
plt.show()