# Importing necessary packages/libraries: 

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import requests
import json
import numpy as np
import pandas
from pandas import DataFrame, to_datetime
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import time
import cgi
import pprint
import os

# Generating the function to employ: 

def output():
    # getting user selections from the index.html page
    selections = request.form.getlist('features')
    ticker = request.form['ticker']
    ticker = ticker.upper()
    #ticker = 'GOOG'
    #selections = ['close']
    
    # Establishing the start and end dates of the stock price data to be displayed in Bokeh plot:
    # Note: the last day of available data with WIKI is 3/27/18. 
    # I assigned days=182 (see below) so that enough data would be plotted, given that today is 6/15/18 
    today_date = datetime.now()
    start_date = (today_date - timedelta(days=365)).strftime('%Y-%m-%d') 
    end_date = today_date.strftime('%Y-%m-%d')
    
    # Pulling the Quandl data    
    quandl_link = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&end_date='+end_date+'&order=asc&api_key=RTKyK2RpPPcGFSMz4NUY'
    r = requests.get(quandl_link)
    #pprint.pprint(r.json())
    
    # Converting data into a Pandas dataframe
    request_df = DataFrame(r.json()) 
    df = DataFrame(request_df.ix['data','dataset'], columns = request_df.ix['column_names','dataset'])
    #print(df)
    df.columns = [x.lower() for x in df.columns]
    df = df.set_index(['date'])
    df.index = to_datetime(df.index)


    # Generating Bokeh plots:
    #output_file("output.html", title="Stock prices changes for last month")
    if 'open' in selections:
        p = figure(x_axis_type = "datetime", title='%s: Opening Price Over Time' %(ticker))
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price (in US dollars)'
        p.line(df.index, df['open'], color='blue', legend='Opening price')
    if 'high' in selections:
        p = figure(x_axis_type = "datetime", title='%s: Highest Price Over Time' %(ticker))
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price (in US dollars)'
        p.line(df.index, df['high'], color='red', legend='Highest price')
    if 'close' in selections:
        p = figure(x_axis_type = "datetime", title='%s: Closing Price Over Time' %(ticker))
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price (in US dollars)'
        p.line(df.index, df['close'], color='purple', legend='Closing price')
    return p

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('indexxx.html')

@app.route('/output',methods=['GET','POST'])
def chart():
    plot = output()
    script, div = embed.components(plot)
    return render_template('output.html', script=script, div=div)

if __name__ == '__main__':
    #app.run(debug = True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)