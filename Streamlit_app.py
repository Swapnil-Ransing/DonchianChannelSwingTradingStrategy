# This file is the app python file to be run from the terminal
import streamlit as st
st.set_page_config(layout="wide") # Uing the wide page layout
from FunctionsFile import *

# setting up a title and description for the app
st.header("Trading stock pick based on Donchian Strategy", divider='rainbow')
st.text("Donchian strategy with different variations will be tested for list of stocks.")
st.text("Based on the strategy results, this app provides an interactive GUI to further select "
        "the list of stocks and then refine the strategy variables to get best output.")


st.subheader("List of stock that this strategy evaluates consists of :")

# Displaying the list of tickers
# ticker_lst=['HDFCBANK','ICICIBANK','FINEORG']
# ticker_lst=['HDFCBANK','ICICIBANK','FINEORG']
ticker_lst=['HDFCBANK',
            'BAJFINANCE',
            'RELIANCE',
            'ASIANPAINT',
            'BALKRISIND',
            'NAUKRI',
            'TATAPOWER',
            'POLYCAB',
            'STARHEALTH',
            'LALPATHLAB',
            'IDFCFIRSTB',
            'DMART',
            'TITAN',
            'PIIND',
            'ICICIBANK',
            'FINEORG',
            'BHARTIARTL',
            'MUTHOOTFIN',
            'TORNTPOWER',
            'AMBUJACEM',
            'DEEPAKNTR',
            'DIVISLAB',
            'GSPL',
            'POWERGRID',
            'NAVINFLUOR',
            # 'SENCO',
            'SONACOMS',
            'INDIAMART',
            # 'AVALON',
            'MANYAVAR',
            'BLUEDART',
            'MAPMYINDIA',
            'CAMPUS',
            'SYNGENE',
            'CARBORUNIV',
            'SOLARINDS',
            'RBA']
for i in ticker_lst:
    st.markdown("- " + i)

st.subheader("Please provide the following inputs to filter the stocks:")
st.text("Buy Signal: Whether the trade is Open or Close")
st.text("CMP_Bp_diff_pct (int) : PCT Difference between CMP and signal Buy price (Results will be less than selected)")
st.text("CAGR (int): Min. CAGR that strategy should have generated")
st.text("Buy_Date (yyyy-mm-dd): Buy signal date (Results will be greater than selected)")

# User Input Buttons
Buy_Signal = st.radio("Buy Signal: ",["Open","Close"])
CMP_Bp_diff_pct = st.number_input('CMP_Bp_diff_pct', min_value=-100, max_value=100, value=5, step=1)
CAGR = st.number_input('CAGR', min_value=-100, max_value=100, value=5, step=1)
Buy_Date = st.text_input("Buy_Date: ",'2023-12-20')

if st.button("Submit", key='my_button_1'):
    # Generate results for large number of stocks
    multiple_stocks_df_daily=buy_alert(ticker_lst,
                                       start='2000-01-01',
                                       investment=100000,
                                       print_results='No',
                                       macd_diff=-5,
                                       stop_loss=8,
                                       Daily='Yes')
    # understand the percentage difference between buy price and CMP
    multiple_stocks_df_daily['CMP_Bp_diff_pct']=round((multiple_stocks_df_daily['CMP']-multiple_stocks_df_daily['Buy_Price'])/multiple_stocks_df_daily['Buy_Price']*100,2)

    # Filter the stocks based on user input
    multiple_stocks_df_daily_filtered = multiple_stocks_df_daily[
        (multiple_stocks_df_daily['Buy_Signal'] == Buy_Signal)
        & (multiple_stocks_df_daily['CMP_Bp_diff_pct'] <= CMP_Bp_diff_pct)
        & (multiple_stocks_df_daily['Buy_Date'] >= Buy_Date)
        & (multiple_stocks_df_daily['CAGR'] >= CAGR)]

    st.dataframe(multiple_stocks_df_daily_filtered)

    st.write('Filtered list of stock is ',list(set(multiple_stocks_df_daily_filtered['Stock'])))

# Refining the strategy parameters for best output of selected stock
st.subheader("Refining and finalizing the strategy parameters for best output of selected stock", divider='rainbow')
st.subheader("Please provide the following inputs to refine the stocks output:")
st.text("Ticker Name: NSE name of the stock in capital")
st.text("Backtest start date (yyyy-mm-dd): Backtesting start date")
st.text("Initial investment amount (int)")
# st.text("Print Results : whether to print the detailed results or not")
st.text("MACD Difference (int) : Diffenrence between signal and macd line")
st.text("Stop Loss (int)")

Ticker_Name=st.text_input("Ticker Name :",'ICICIBANK')
Backtest_start_Date=st.text_input("Backtest start date :",'2000-01-01')
investment=st.number_input('Initial investment amount :',100000)
# print_results = st.radio("Print Results : ",["No","Yes"])
macd_dif=st.number_input("MACD Difference :",-5)
stop_loss=st.number_input("Stop Loss :",8)

if st.button("Refine", key='my_button_2'):
    # Refined stock on daily basis results
    ref_stock_daily = automate_strategies(ticker=Ticker_Name,
                                      start=Backtest_start_Date,
                                      investment=investment,
                                      print_results="No",
                                      macd_diff=macd_dif,
                                      stop_loss=stop_loss,
                                      Daily='Yes')
    # Refined stock on weekly basis results
    ref_stock_weekly = automate_strategies(ticker=Ticker_Name,
                                      start=Backtest_start_Date,
                                      investment=investment,
                                      print_results="No",
                                      macd_diff=macd_dif,
                                      stop_loss=stop_loss,
                                       Daily='No')

    st.text("Backtesting results for Daily data :")
    st.dataframe(ref_stock_daily)
    st.text("Backtesting results for Weekly data :")
    st.dataframe(ref_stock_weekly)
    st.text("Stock refinement results are completed")

# Printing the detailed trades of finalized strategy
st.subheader("Printing the detailed trades of finalized strategy", divider='rainbow')
daily_weekly = st.radio("Daily or Weekly Price : ",["Daily","Weekly"])
final_strategy = st.radio("Daily or Weekly Price : ",["Plain","Reverse","RevMACD"])

if st.button("Get Detailed Trades", key='my_button_3'):
    df = pdr.get_data_yahoo(str(Ticker_Name + ".NS"), start=Backtest_start_Date)
    # Getting the weekly data for weekly detailed
    if daily_weekly == 'Weekly':
        df = df.resample("W-MON").last()

    # CALCULATING DONCHIAN CHANNEL and Moving Averages
    df[['dcl', 'dcm', 'dcu']] = df.ta.donchian(lower_length=40, upper_length=50)
    df['Fast_EMA'] = df['Close'].ewm(span=20, adjust=False).mean()  # Fast exponential moving average
    df['Slow_EMA'] = df['Close'].ewm(span=50, adjust=False).mean()  # Slow exponential moving average
    df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)

    if final_strategy == 'Plain':
        donchian_plain_st(aapl=df, investment=investment, print_results='Yes')
    elif final_strategy == 'Reverse':
        donchian_reverse_st(aapl=df, investment=investment, print_results='Yes')
    elif final_strategy == 'RevMACD':
        donchian_reverse_macd_st(df, investment=investment, macd_signal_diff=macd_dif,
                              stop_loss_pct=stop_loss, print_results='Yes')
