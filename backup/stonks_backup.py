import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import datetime

#!stock <stock_name> <period(1d,5d,1mo,3mo,6mo,1y,2y,5y,10y)> custom_stock()
#!stoncks <date(yyyy-mm-dd)> predefinded_stocks()

def custom_stock(stock,stock_period):
    stock_interval='1m'
    data=yf.download(tickers=stock.upper(),period=stock_period,interval=stock_interval)['Close']
    data.plot(figsize=(10,7))
    plt.legend()
    plt.title("CASH",fontsize=16)
    plt.ylabel('Returns',fontsize=14)
    plt.xlabel('Time',fontsize=14)
    plt.grid(which="major",color='k',linestyle='-.',linewidth=0.5)   
    #plt.show()
    plt_name='custom_stock_'+stock+'_'+str(datetime.datetime.today())+'.png'
    plt.savefig(plt_name)
    return plt_name
    
    

def predefinded_stocks(date):
    stocks=["ocgn","asxc","admp","san.pa","goog"]
    data=yf.download(stocks,date)['Close']

    ((data.pct_change()+1).cumprod()).plot(figsize=(10,7))
    plt.legend()
    plt.title("CASH",fontsize=16)
    plt.ylabel('Returns',fontsize=14)
    plt.xlabel('Time',fontsize=14)
    plt.grid(which="major",color='k',linestyle='-.',linewidth=0.5)
    #plt.show()
    plt_name='pre_stock_'+str(datetime.datetime.today())+'.png'
    plt.savefig(plt_name)
    return plt_name
    
    
#custom_stock('ocgn',stock_period='1d')
#predefinded_stocks('2020-01-01')