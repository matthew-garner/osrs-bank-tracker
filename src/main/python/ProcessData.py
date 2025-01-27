import pandas as pd
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.dates as mdates
import numpy as np

def LoadData():
    df = pd.read_pickle("resources/pythondata/priceSeriesCollection.pkl")
    return df

def ConvertTimeSeries(timeSeries):
    for item in timeSeries:
        item['timestamp'] = datetime.fromtimestamp(item['timestamp']).date()
    return timeSeries

def getTimeSeriesItem(i):
    timeSeries = df["timeseries"][i]
    return timeSeries

def getItemPriceData(timeSeries, price): #price: 'avgLowPrice' or 'avgHighPrice'
    timeStamps = [record["timestamp"] for record in timeSeries]
    prices = [record[price] for record in timeSeries]
    return prices, timeStamps

def bankValueTotal():
    allPrices = []
    for i in range(len(df)):
        timeSeries = getTimeSeriesItem(i)
        prices, timeStamps = getItemPriceData(timeSeries, "avgHighPrice")
        allPrices.append(prices)
    dfAllPrices = pd.DataFrame(allPrices)
    dfAllPrices = dfAllPrices.fillna(0)
    columnSum = dfAllPrices.sum(axis=0)
    #max_length = min(len(row) for row in allPrices)
    return columnSum.tolist(), timeStamps


df = LoadData()
#x = getTimeSeriesItem(1)
#Prices, timeStamps = getItemPriceData(x, "avgHighPrice")

totalValue, timeStamps = bankValueTotal()


fig = px.line(x = timeStamps, y = totalValue,
    labels={"x": "Date", "y": "Avg High Price"},
    title="Price Series"
)
fig.show()

