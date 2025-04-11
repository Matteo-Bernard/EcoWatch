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
    return tbond_df[[col for _, col in mo_cols + yr_cols]]   


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
    df = df.resample('D').ffill()
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
    url = 'https://api.statistiken.bundesbank.de/rest/download/BBSSY/D.REN.EUR.A610.000000WT0202.A?format=csv&lang=en'
    response = requests.get(url)
    content = response.content.decode('utf-8')
    content = csv.reader(content.splitlines(), delimiter=',')
    df = pd.DataFrame(list(content))
    df = df.set_index(0)
    df = df.iloc[9:,0]
    df = df.replace(".", np.nan).dropna()
    df.name = 'Bunds 2 Yr'
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

def fedfunds(ticker='EFFR', start='2000-01-01', end='2025-01-01'):
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
    ticker_dict = {
        'EFFR': '500',
        'OBFR': '505',
        'TGCR': '510',
        'BGCR': '515',
        'SOFR': '520',
    }
    url = (f"https://markets.newyorkfed.org/read?startDt={start}&endDt={end}&eventCodes={ticker_dict[ticker]}&productCode=50&sort=postDt:-1,eventCode:1&format=csv")
    response = requests.get(url)
    csv_file = io.StringIO(response.text)
    data = pd.read_csv(csv_file, index_col='Effective Date')
    data.index = pd.to_datetime(data.index)
    data = data.drop(columns=['Rate Type'])
    return data