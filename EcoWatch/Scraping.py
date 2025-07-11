from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import numpy as np
import requests
import io
import csv

def tbond(first_year, last_year):
    tbond_df = pd.DataFrame()
    for year in range(int(first_year), int(last_year) + 1):
        url = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv'
        response = requests.get(url, headers={'User-Agent': 'Safari/537.36'}, timeout=10)
        csv_file = io.StringIO(response.text)
        data = pd.read_csv(csv_file, index_col='Date')
        data.index = pd.to_datetime(data.index)
        tbond_df = pd.concat([tbond_df, data], axis=0)
    
    # Sort and fill missing values
    tbond_df = tbond_df.sort_index()
    tbond_df = tbond_df.resample('D').ffill()

    # Sort columns : "Mo" first then "Yr"
    mo_cols = []
    yr_cols = []
    for col in tbond_df.columns:
        num, unit = col.split()
        if unit == "Mo":
            mo_cols.append((float(num), col))
        else:
            yr_cols.append((float(num), col))
    mo_cols.sort()
    yr_cols.sort()
    tbond_df = tbond_df[[col for _, col in mo_cols + yr_cols]]  
    tbond_df = tbond_df.drop(columns=('1.5 Month'))
    tbond_df.columns = [mat.replace(' Mo', 'M').replace(' Yr', 'Y') for mat in tbond_df.columns] 
    return tbond_df


def oat():
    url = 'https://webstat.banque-france.fr/export/csv-columns/fr/selection/5385693'
    response = requests.get(url, headers={'User-Agent': 'Safari/537.36'}, timeout= 10)
    csv_file = io.StringIO(response.text)
    df = pd.read_csv(csv_file, header=5, sep = ';')

    # Clean and process the data
    columns = ['Date', '1 Yr', '10 Yr', '15 Yr', '2 Yr', '20 Yr', '25 Yr', '3 Yr', '30 Yr', '5 Yr', '7 Yr']
    df.columns = columns
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index, format='ISO8601')
    df = df.replace('-', np.nan)
    df = df.replace(',', '.', regex=True)
    df = pd.concat([pd.to_numeric(df[col], errors='coerce') for col in df.columns], axis=1)
    
    # Sort and fill missing values
    df = df.sort_index()
    df = df[['1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '15 Yr', '20 Yr', '25 Yr', '30 Yr']]
    df.columns = ['1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '15Y', '20Y', '25Y', '30Y']
    df = df.resample('B').ffill()
    return df.ffill()  

def ester():
    url = 'https://data-api.ecb.europa.eu/service/data/EST/B.EU000A2QQF16.CR?format=csvdata'
    response = requests.get(url)
    content = response.content.decode('utf-8')
    content = csv.reader(content.splitlines(), delimiter=',')
    df = pd.DataFrame(list(content))
    df.columns = df.loc[0]
    df = df.drop(0, axis=0)
    df = df.set_index('TIME_PERIOD')
    df = df['OBS_VALUE']
    df.name = 'ESTER'
    df.index = pd.to_datetime(df.index, format='ISO8601')
    return df.astype(float)

def bunds():    
    urls = {
        '1Y'    : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R01XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '2Y'    : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R02XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '3Y'    : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R03XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '5Y'    : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R05XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '7Y'    : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R07XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '10Y'   : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R10XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '20Y'   : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R20XX.R.A.A._Z._Z.A?format=csv&lang=en',
        '30Y'   : 'https://api.statistiken.bundesbank.de/rest/download/BBSIS/D.I.ZAR.ZI.EUR.S1311.B.A604.R30XX.R.A.A._Z._Z.A?format=csv&lang=en',
    }
    df = pd.DataFrame(columns=urls.keys())
    for mat, url in urls.items():
        response = requests.get(url)
        content = response.content.decode('utf-8')
        content = csv.reader(content.splitlines(), delimiter=',')
        data = pd.DataFrame(list(content))
        data = data.set_index(0)
        data = data.iloc[9:,0]
        data = data.replace(".", np.nan).dropna()
        data.name = mat
        df[mat] = data  
    df.index = pd.to_datetime(df.index, format='ISO8601')
    return df.astype(float)

def fred(key, ticker):
    # Get an economical series
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={ticker}&api_key={key}&file_type=json'
    response = requests.get(url)

    # Clean the response
    df = pd.DataFrame(data=response.json()['observations'])
    df.index = pd.to_datetime(df.date)

    # Transform string into float
    df = df.loc[:,'value']
    df = df[df != "."]
    df = df.astype(float)
    return df

def fed_funds(ticker='EFFR'):
    """
    Fetches historical interest rate data from the New York Federal Reserve's website.

    Parameters:
    - ticker (str): The ticker symbol for the interest rate type. Available options are:
        - 'EFFR': Effective Federal Funds Rate
        - 'OBFR': Overnight Bank Funding Rate
        - 'TGCR': Tri-Party General Collateral Rate
        - 'BGCR': Broad General Collateral Rate
        - 'SOFR': Secured Overnight Financing Rate
      Default is 'EFFR'.
    - start (str): The start date for the data range in 'YYYY-MM-DD' format. Default is '2000-01-01'.
    - end (str): The end date for the data range in 'YYYY-MM-DD' format. Default is '2025-01-01'.

    Returns:
    - pd.DataFrame: A DataFrame containing the interest rate data indexed by date.
    """
    start='2000-01-01'
    end=dt.datetime.now().strftime("%Y-%m-%d")
    ticker_dict = {
        'EFFR': '500',
        'OBFR': '505',
        'TGCR': '510',
        'BGCR': '515',
        'SOFR': '520',
    }
    url = (f"https://markets.newyorkfed.org/read?startDt={start}&endDt={end}&eventCodes={ticker_dict[ticker]}&productCode=50&sort=postDt:1,eventCode:1&format=csv")
    response = requests.get(url)
    csv_file = io.StringIO(response.text)
    data = pd.read_csv(csv_file, index_col='Effective Date')
    data.index = pd.to_datetime(data.index)
    data = data.drop(columns=['Rate Type'])
    return data

import requests
from bs4 import BeautifulSoup
import pandas as pd

def ecb(ticker):
    headers = {"Accept": "application/vnd.sdmx.structurespecificdata+xml;version=2.1"}
    key = ticker.partition('.')[0] + '/' + ticker.partition('.')[2]
    url = f'https://data-api.ecb.europa.eu/service/data/{key}?format=xml'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content,'xml')
    data = [
        {'Date': obs['TIME_PERIOD'], 'Value': float(obs['OBS_VALUE'])}
        for obs in soup.find_all('Obs')
    ]
    df = pd.DataFrame(data, columns=['Date', 'Value'])
    df = df.set_index('Date', drop=True)
    df.index = pd.to_datetime(df.index)
    return df

import pandas as pd
import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def cnn():
    # Configuration du navigateur
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")

    # Initialisation du driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL cible
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

    # Ouverture de la page
    driver.get(url)
    time.sleep(2)

    # Récupération brute du texte JSON
    json_raw = driver.find_element(By.TAG_NAME, "pre").text
    json_clean = json.loads(json_raw)
    driver.quit()

    dict = {
        'Fear and Greed'       : 'fear_and_greed_historical', 
        'Market Momentum SP500' : 'market_momentum_sp500', 
        'Stock Price Strength'  : 'stock_price_strength', 
        'Stock Price Breadth'   : 'stock_price_breadth', 
        'Put Call Options'      : 'put_call_options', 
        'Market Volatility VIX' : 'market_volatility_vix',
        'Junk Bond Demand'      : 'junk_bond_demand', 
        'Safe Haven Demand'     : 'safe_haven_demand'
    }
    index = pd.DataFrame(json_clean['fear_and_greed_historical']['data'])['x']
    columns = dict.keys()
    df = pd.DataFrame(index=index, columns=columns)

    for name, ticker in dict.items():
        data = pd.DataFrame(json_clean[ticker]['data'])
        data = data.set_index('x', drop=True)
        df[name] = data['y']
        df[f'{name} Rating'] = data['rating']
    
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.resample('B').last()
    df = df.dropna()

    return df

import pandas as pd
import requests

def eia(key, route, contract, product):
    url = f'https://api.eia.gov/v2/{route}/pri/{contract}/data/?frequency=daily&data[0]=value&facets[product][]={product}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={key}'
    json = requests.get(url=url).json()
    data = pd.DataFrame(json['response']['data'])
    data = data.set_index('period')
    data = data['value']
    data.index = pd.to_datetime(data.index)
    data = data.sort_index(ascending=True)
    data = data.groupby(data.index).last()
    data = data.dropna()
    data = data.resample('B').ffill()
    data = data.astype(float)
    return data

from binance.client import Client
import pandas as pd
import datetime as dt

def binance(key, secret, symbol, start, end):
    client = Client(key, secret)
    interval = Client.KLINE_INTERVAL_1DAY
    start_str = str(dt.datetime.strptime(start, '%Y/%m/%d'))
    end_str = str(dt.datetime.strptime(end, '%Y/%m/%d'))
    klines = client.get_historical_klines(
        symbol=symbol, 
        interval=interval, 
        start_str=start_str, 
        end_str=end_str
    )
    columns  =['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(klines, columns=columns)

    columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']

    for col in columns_to_convert:
        df[col] = df[col].astype(float)

    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
    df = df.set_index('Open Time', drop=True)

    return df
