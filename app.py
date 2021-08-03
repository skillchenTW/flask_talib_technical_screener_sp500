import yfinance as yf
import os, csv
import pandas as pd
import talib
from flask import Flask,render_template,request
from .pattern import patterns

app = Flask(__name__)


@app.route("/")
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}
    with open('datasets/sp500_companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = { 'company': row[1] }
    print(stocks)        
    if pattern:
        datafiles = os.listdir('datasets/daily')
        for filename in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            try:
                result = pattern_function(df['Open'],df['High'],df['Low'],df['Close'])               
                last = result.tail(1).values[0]
                #print(last)
                if last >0 :
                    stocks[symbol][pattern] ='Bullish'
                elif last <0 :
                    stocks[symbol][pattern] ='Bearish'
                else:
                    stocks[symbol][pattern] = None
                    #print("{} triggered {}".format(filename, pattern))
            except:
                pass
    return render_template("index.html",patterns=patterns, stocks=stocks, current_pattern=pattern)

@app.route('/snapshot')
def snapshot():
    with open('datasets/sp500_companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]            
            df = yf.download(symbol, start="2020-01-01", end="2021-08-02")
            df.to_csv('datasets/daily/{}.csv'.format(symbol))
            
           
       


