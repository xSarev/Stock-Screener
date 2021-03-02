from keys import ameritrade
import plotly.graph_objects as go
import plotly.express as px
import requests, time, re, pickle
import pandas
import os

files_data = []

def writeStockData():
    url = "https://api.tdameritrade.com/v1/instruments"

    stock_list = pandas.read_csv('company_lists.csv', usecols=['Symbol']).values.tolist()

    start = 0
    end = 500

    while start < len(stock_list):
        if len(stock_list) < end:
            symbols = stock_list[start:len(stock_list)]
        else:
            symbols = stock_list[start:end]
        
        payload = {'apikey': ameritrade["Consumer Key"],
                   'symbol': symbols,
                   'projection': 'fundamental'}

        results = requests.get(url, params=payload)

        data = results.json()
        file_name = str(time.asctime()) + '.pkl'
        file_name = re.sub('[ :]', '_', file_name)

        files_data.append(file_name)

        with open(file_name, 'wb') as file:
            pickle.dump(data, file)
        start = end
        end += 500
        time.sleep(1)


def readStockDataFromFile():
    data = []

    for file in files_data:
        with open(file, 'rb') as f:
            info = pickle.load(f)
        stocks_keys = list(info)

        # Points of interest for stocks
        points = ['symbol', 'netProfitMarginMRQ', 'peRatio', 'pegRatio', 'high52', 'dividendAmount']
        for stock in stocks_keys:
            stock_data = []
            for point in points:
                stock_data.append(info[stock]['fundamental'][point])
            data.append(stock_data)
        os.remove(file)
    return data


def createScreneerTable():
    data = readStockDataFromFile()

    # New columns for data to be displayed
    columns = ['Symbol', 'Margin', 'PE', 'PEG', 'high52', 'Dividend']
    file_results = pandas.DataFrame(data, columns=columns)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=columns,
            line_color='paleturquoise',
            align='center'
        ),
        cells=dict(
            values=[
            file_results.Symbol,
            file_results.Margin,
            file_results.PE,
            file_results.PEG,
            file_results.high52,
            file_results.Dividend]
            ))
        ])

    fig.show()

if __name__ == '__main__':
    writeStockData()
    createScreneerTable()