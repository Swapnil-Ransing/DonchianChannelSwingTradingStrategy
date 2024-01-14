
# Lets import the packages and functions
# Install the packages within python code
import streamlit as st
import subprocess
import sys

def install_c(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_c("tabulate")
install_c("pandas_datareader")
install_c("yfinance")
install_c("pandas_ta")
install_c("termcolor")

import numpy as np
from tabulate import tabulate
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import pandas_ta as ta
import math
from termcolor import colored as cl

import warnings
warnings.filterwarnings("ignore")

## Donchian strategy functions
# Strategy 1 Function : Plain Donchian Strategy
def donchian_plain(aapl, investment, print_results):

    in_position = False
    equity = investment
    Total_trades=0
    Successful_trades=0
    buy_price=0
    buy_signal_alert='Open'

    for i in range(3, len(aapl)):
        if aapl['High'][i] == aapl['dcu'][i] and in_position == False:
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price = aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            if print_results == 'Yes':
              print(cl('BUY: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        elif aapl['Low'][i] == aapl['dcl'][i] and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
              print(cl('SELL: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
          print(cl(f'\nClosing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}', attrs = ['bold']))
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      print(cl(f'EARNING: {earning} ;Investment Price: {round(equity,1)}; CAGR: {CAGR} ; ROI: {roi}%', attrs = ['bold']))
      print(cl(f'Total Trades: {Total_trades}; Success Ratio : {round(Successful_trades/Total_trades*100,2)}', attrs = ['bold']))
    current_price=round(aapl.Close[i],2)
    return [round(equity,1),roi,CAGR,round(Successful_trades/Total_trades*100,2),buy_date,round(buy_price,2),current_price,buy_signal_alert]

# Strategy 2: Rev Donchian strategy
def donchian_reverse(aapl, investment,print_results):

    in_position = False
    equity = investment
    Total_trades=0
    Successful_trades=0
    buy_price=0
    buy_signal_alert='Open'

    for i in range(3, len(aapl)):
        if aapl['Low'][i] == aapl['dcl'][i] and in_position == False:
            no_of_shares = math.floor(equity/aapl.Close[i])
            equity -= (no_of_shares * aapl.Close[i])
            buy_price = aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            in_position = True
            if print_results == 'Yes':
              print(cl('BUY: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        elif aapl['High'][i] == aapl['dcu'][i] and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
              print(cl('SELL: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
          print(cl(f'\nClosing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}', attrs = ['bold']))
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      print(cl(f'EARNING: {earning} ;Investment Price: {round(equity,1)}; CAGR: {CAGR} ; ROI: {roi}%', attrs = ['bold']))
      print(cl(f'Total Trades: {Total_trades}; Success Ratio : {round(Successful_trades/Total_trades*100,2)}', attrs = ['bold']))
    current_price=round(aapl.Close[i],2)
    return [round(equity,1),roi,CAGR,round(Successful_trades/Total_trades*100,2),buy_date,round(buy_price,2),current_price,buy_signal_alert]

# Strategy 3 : Rev Donchian Strategy with MACD
# BACKTESTING THE STRATEGY

def donchian_reverse_macd(aapl, investment,macd_signal_diff,stop_loss_pct,print_results):

    in_position = False
    equity = investment
    buy_signal = False
    sell_based_macd= False
    buy_price=0
    Total_trades=0
    Successful_trades=0
    buy_signal_alert='Open'

    for i in range(50, len(aapl)):
        # Buy if low price is at dcl and MACDh_12_26_9 > 0
        if aapl['Low'][i] == aapl['dcl'][i] and in_position == False:
            buy_signal = True
            if aapl['MACDh_12_26_9'][i] > macd_signal_diff:
              no_of_shares = math.floor(equity/aapl.Close[i])
              buy_price=aapl.Close[i]
              buy_date = str(aapl.index[i])[:10]
              equity -= (no_of_shares * aapl.Close[i])
              in_position = True
              if print_results == 'Yes':
                print(cl('Buy: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on price')
        # Buy when buy_signal is True now however buy did not happened becaseue of MACDh_12_26_9 < 0 in previous situation
        elif buy_signal == True and in_position == False and aapl['Low'][i] >= aapl['dcl'][i] and aapl['MACDh_12_26_9'][i] > macd_signal_diff:
        # elif buy_signal == True and in_position == False and aapl['MACDh_12_26_9'][i] > macd_signal_diff:
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price=aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            buy_signal = False
            if print_results == 'Yes':
              print(cl('Buy: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on price and buy signal')
        # Sell when MACDh_12_26_9 < 0
        elif aapl['MACDh_12_26_9'][i] < macd_signal_diff and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            sell_based_macd= True
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
              print(cl('Sell: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are sold at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on MACD')
        # Sell when stoploss is reached
        elif aapl['Close'][i] < (buy_price*(1-(stop_loss_pct/100))) and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
              print(cl('Sell: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are sold at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on Stop Loss')
        # Buy when position is sold because of MACDh_12_26_9 < 0 and high is not achieved and now MACDh_12_26_9 > 0
        elif sell_based_macd == True and aapl['MACDh_12_26_9'][i] > macd_signal_diff and aapl['Low'][i] > aapl['dcl'][i] and in_position == False :
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price=aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            if print_results == 'Yes':
              print(cl('Buy: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on buy st 2')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
          print(cl(f'\nClosing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}', attrs = ['bold']))
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      print(cl(f'EARNING: {earning} ;Investment Price: {round(equity,1)}; CAGR: {CAGR} ; ROI: {roi}%', attrs = ['bold']))
      print(cl(f'Total Trades: {Total_trades}; Success Ratio : {round(Successful_trades/Total_trades*100,2)}', attrs = ['bold']))
    current_price=round(aapl.Close[i],2)
    return [round(equity,1),roi,CAGR,round(Successful_trades/Total_trades*100,2),buy_date,round(buy_price,2),current_price,buy_signal_alert]

# Automating all 3 strategies for a single ticker
def automate_strategies(ticker,start,investment,print_results,macd_diff,stop_loss,Daily):
  """
  This function runs all the three developed Donchian strategies and outputs the dataframe with results of these strategies.
  Input:
  ticker : NSE name of a stock
  start : Start time of a stock trade for backtesting
  investment : initial investment amount
  print_results : Yes/No value for printing the intermediate buy sell results
  macd_diff : for 3rd strategy buy or sell will happen based on this difference
  stop_loss : for 3rd strategy, stop loss for sell signal
  Daily : Yes/No for daily or weekly price actions

  """

  # Getting the stock data
  df = pdr.get_data_yahoo(str(ticker+".NS"), start=start)

  if Daily != 'Yes' :
    # Getting the weekly data
    df = df.resample("W-MON").last()

  # CALCULATING DONCHIAN CHANNEL and Moving Averages
  df[['dcl', 'dcm', 'dcu']] = df.ta.donchian(lower_length = 40, upper_length = 50)
  df['Fast_EMA']=df['Close'].ewm(span = 20, adjust = False).mean() # Fast exponential moving average
  df['Slow_EMA']=df['Close'].ewm(span = 50, adjust = False).mean() # Slow exponential moving average
  # # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
  # macd = k - d
  # # Get the 9-Day EMA of the MACD for the Trigger line
  # macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
  # # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
  # macd_h = macd - macd_s
  df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)

  # defining a dataframe to store the results
  result_df=pd.DataFrame(columns=['Stock','Strategy','Investment','Total_Years','Final_Price','ROI','CAGR','Success_Ratio','Buy_Date','Buy_Price','CMP','Buy_Signal'])

  # Strategy 1 - Plain
  results_lst=[ticker,'Plain',investment,df.index[-1].year-df.index[0].year]
  res = donchian_plain(df, investment,print_results)
  results_lst.extend(res)
  #Append the results to the dataframe
  result_df.loc[len(result_df)] = results_lst

  # Strategy 2 - Reverse
  results_lst=[ticker,'Reverse',investment,df.index[-1].year-df.index[0].year]
  res = donchian_reverse(df, investment,print_results)
  results_lst.extend(res)
  #Append the results to the dataframe
  result_df.loc[len(result_df)] = results_lst

  # Strategy 3 - Reverse with MACD
  results_lst=[ticker,'RevMACD',investment,df.index[-1].year-df.index[0].year]
  res = donchian_reverse_macd(df, investment,macd_diff,stop_loss,print_results)
  results_lst.extend(res)
  #Append the results to the dataframe
  result_df.loc[len(result_df)] = results_lst

  return result_df

# Automating the strategies for multiple stocks
def automate_multiplestocks(ticker_lst,start,investment,print_results,macd_diff,stop_loss,Daily):

  """
  This function runs all the three developed Donchian strategies for multiple stocks and outputs the dataframe with results of these strategies.
  Input:
  ticker_lst : list of NSE name of a stock
  start : Start time of a stock trade for backtesting
  investment : initial investment amount
  print_results : Yes/No value for printing the intermediate buy sell results
  macd_diff : for 3rd strategy buy or sell will happen based on this difference
  stop_loss : for 3rd strategy, stop loss for sell signal
  Daily : Yes/No for daily or weekly price actions

  """

  # Defining the results dataframe to store all stocks data
  result_df=pd.DataFrame(columns=['Stock','Strategy','Investment','Total_Years','Final_Price','ROI','CAGR','Success_Ratio','Buy_Date','Buy_Price','CMP','Buy_Signal'])

  for ele in ticker_lst:
    res_df = automate_strategies(ele,start,investment,print_results,macd_diff,stop_loss,Daily)
    # concat the single stock results dataframe to the main dataframe
    result_df = pd.concat([result_df, res_df], ignore_index=True)

  return result_df

# Buy alert generation
def buy_alert(ticker_lst,start,investment,print_results,macd_diff,stop_loss,Daily):

  """
  This function runs all the three developed Donchian strategies for multiple stocks.
  Amongst these three results it finds the best strategy
  and then outputs the results for best strategy with buy signal if any.

  Input:
  ticker_lst : list of NSE name of a stock
  start : Start time of a stock trade for backtesting
  investment : initial investment amount
  print_results : Yes/No value for printing the intermediate buy sell results
  macd_diff : for 3rd strategy buy or sell will happen based on this difference
  stop_loss : for 3rd strategy, stop loss for sell signal
  Daily : Yes/No for daily or weekly price actions

  """

  # Defining the results dataframe to store all stocks data
  result_df=pd.DataFrame(columns=['Stock','Strategy','Investment','Total_Years','Final_Price','ROI','CAGR','Success_Ratio','Buy_Date','Buy_Price','CMP','Buy_Signal'])

  for ele in ticker_lst:
    res_df = automate_strategies(ele,start,investment,print_results,macd_diff,stop_loss,Daily)
    # # Keep only the best strategy of a ticker
    # filt = (res_df['CAGR'] == res_df.CAGR.max())
    # res_df_subset = res_df[filt]

    # append the single stock best strategy results dataframe to the main dataframe
    result_df = pd.concat([result_df, res_df], ignore_index=True)
    print('Completed : ',ele)

  return result_df


# Strategy 1 Function : Plain Donchian Strategy for streamlit printing
def donchian_plain_st(aapl, investment, print_results):

    in_position = False
    equity = investment
    Total_trades=0
    Successful_trades=0
    buy_price=0
    buy_signal_alert='Open'

    for i in range(3, len(aapl)):
        if aapl['High'][i] == aapl['dcu'][i] and in_position == False:
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price = aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            if print_results == 'Yes':
                st.write(f'BUY: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        elif aapl['Low'][i] == aapl['dcl'][i] and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
                st.write(f'SELL: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
            st.write(f'Closing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      st.write(f'EARNING: **{earning}** ;Investment Price: **{round(equity,1)}**; CAGR: **{CAGR}** ; ROI: **{roi}**%')
      st.write(f'Total Trades: **{Total_trades}**; Success Ratio : **{round(Successful_trades/Total_trades*100,2)}**')

# Strategy 2: Rev Donchian strategy for streamlit printing
def donchian_reverse_st(aapl, investment,print_results):

    in_position = False
    equity = investment
    Total_trades=0
    Successful_trades=0
    buy_price=0
    buy_signal_alert='Open'

    for i in range(3, len(aapl)):
        if aapl['Low'][i] == aapl['dcl'][i] and in_position == False:
            no_of_shares = math.floor(equity/aapl.Close[i])
            equity -= (no_of_shares * aapl.Close[i])
            buy_price = aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            in_position = True
            if print_results == 'Yes':
              st.write(f'BUY: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        elif aapl['High'][i] == aapl['dcu'][i] and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
              st.write(f'SELL: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
          st.write(f'Closing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      st.write(f'EARNING: **{earning}** ;Investment Price: **{round(equity,1)}**; CAGR: **{CAGR}** ; ROI: **{roi}**%')
      st.write(f'Total Trades: **{Total_trades}**; Success Ratio : **{round(Successful_trades/Total_trades*100,2)}**')


# Strategy 3 : Rev Donchian Strategy with MACD for streamlit printing
# BACKTESTING THE STRATEGY

def donchian_reverse_macd_st(aapl, investment,macd_signal_diff,stop_loss_pct,print_results):

    in_position = False
    equity = investment
    buy_signal = False
    sell_based_macd= False
    buy_price=0
    Total_trades=0
    Successful_trades=0
    buy_signal_alert='Open'

    for i in range(50, len(aapl)):
        # Buy if low price is at dcl and MACDh_12_26_9 > 0
        if aapl['Low'][i] == aapl['dcl'][i] and in_position == False:
            buy_signal = True
            if aapl['MACDh_12_26_9'][i] > macd_signal_diff:
              no_of_shares = math.floor(equity/aapl.Close[i])
              buy_price=aapl.Close[i]
              buy_date = str(aapl.index[i])[:10]
              equity -= (no_of_shares * aapl.Close[i])
              in_position = True
              if print_results == 'Yes':
                  st.write(f'Buy: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on price')
        # Buy when buy_signal is True now however buy did not happened becaseue of MACDh_12_26_9 < 0 in previous situation
        elif buy_signal == True and in_position == False and aapl['Low'][i] >= aapl['dcl'][i] and aapl['MACDh_12_26_9'][i] > macd_signal_diff:
        # elif buy_signal == True and in_position == False and aapl['MACDh_12_26_9'][i] > macd_signal_diff:
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price=aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            buy_signal = False
            if print_results == 'Yes':
                st.write(f'Buy: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on price and buy signal')
        # Sell when MACDh_12_26_9 < 0
        elif aapl['MACDh_12_26_9'][i] < macd_signal_diff and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            sell_based_macd= True
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
                st.write(f'Sell: {no_of_shares} Shares are sold at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on MACD')
        # Sell when stoploss is reached
        elif aapl['Close'][i] < (buy_price*(1-(stop_loss_pct/100))) and in_position == True:
            equity += (no_of_shares * aapl.Close[i])
            in_position = False
            Total_trades += 1
            if buy_price < aapl.Close[i] :
              Successful_trades += 1
            if print_results == 'Yes':
                st.write(f'Sell: {no_of_shares} Shares are sold at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on Stop Loss')
        # Buy when position is sold because of MACDh_12_26_9 < 0 and high is not achieved and now MACDh_12_26_9 > 0
        elif sell_based_macd == True and aapl['MACDh_12_26_9'][i] > macd_signal_diff and aapl['Low'][i] > aapl['dcl'][i] and in_position == False :
            no_of_shares = math.floor(equity/aapl.Close[i])
            buy_price=aapl.Close[i]
            buy_date = str(aapl.index[i])[:10]
            equity -= (no_of_shares * aapl.Close[i])
            in_position = True
            if print_results == 'Yes':
                st.write(f'Buy: {no_of_shares} Shares are bought at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]} based on buy st 2')
    if in_position == True:
        equity += (no_of_shares * aapl.Close[i])
        Total_trades += 1
        if buy_price < aapl.Close[i] :
          Successful_trades += 1
        if print_results == 'Yes':
            st.write(f'Closing position at {round(aapl.Close[i],2)} on {str(aapl.index[i])[:10]}')
        in_position = False

    elif in_position == False:
      # This means position is closed and no buy signal is present. Correct the buy signal attibute to complete
      buy_signal_alert='Close'

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    # CAGR Calculation
    total_years=aapl.index[-1].year-aapl.index[0].year
    CAGR=round(((equity/investment)**(1/total_years)-1)*100,2)
    if print_results == 'Yes':
      st.write(f'EARNING: **{earning}** ;Investment Price: **{round(equity,1)}**; CAGR: **{CAGR}** ; ROI: **{roi}**%')
      st.write(f'Total Trades: **{Total_trades}**; Success Ratio : **{round(Successful_trades/Total_trades*100,2)}**')