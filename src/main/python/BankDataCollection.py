import pandas as pd
import requests
import json
from datetime import datetime
from ProcessData import ConvertTimeSeries

headers = {
    'User-Agent': 'catcat572',
    'From': 'matthewgarner572@gmail.com'  # This is another valid field
}
data = "https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=24h&id="
dfBank = pd.read_csv("resources/output.csv")

def FetchTimeSeries(itemID):
    response = requests.get(f"{data}{itemID}", headers=headers)
    timeSeriesData = response.json()["data"]
    return timeSeriesData


def ConstructDf():
    dfBank["timeseries"] = None
    for index, row in dfBank.iterrows():
        itemID = row["Item ID"]
        timeSeriesData = FetchTimeSeries(itemID)
        if timeSeriesData:
            dfBank.at[index, "timeseries"] = ConvertTimeSeries(timeSeriesData)
        else:
            dfBank.at[index, "timeseries"] = []
    return dfBank

df = ConstructDf()
df.to_pickle("resources/pythondata/priceSeriesCollection.pkl")


