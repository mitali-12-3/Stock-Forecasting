import streamlit as st 
import pandas as pd 
import yfinance as yf
import datetime 
from datetime import date
from prophet import Prophet 
from prophet.plot import plot_plotly  # plotly library for prophet model plotting
import time 
from streamlit_option_menu import option_menu  
import plotly.graph_objects as go

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Sidebar Section Starts Here
today = date.today()  # today's date
st.write('''# StockProject ''')  # title
st.sidebar.image(r"img.png", width=250, use_column_width=False)  # logo
st.sidebar.write('''# StockProject ''')

with st.sidebar: 
    selected = option_menu("Utilities", ["Real-Time Stocks", "Stock Price Prediction", 'About project'])

start = st.sidebar.date_input('Start', datetime.date(2024, 7, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
# Sidebar Section Ends Here

# read csv file
stock_df = pd.read_csv(r"Data.csv")

# Real-Time Stock Price Section Starts Here
if selected == 'Real-Time Stocks':
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)
    with st.spinner('Loading...'): 
        time.sleep(1)
    dict_csv = pd.read_csv(r"Data.csv", header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list
    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false
    def callback():  # function for updating data
        st.session_state.button_clicked = True  # set button clicked to true
    if (st.button("Search", on_click=callback)  # button for searching data
        or st.session_state.button_clicked):  # if button is clicked
        if a == "":  # if user doesn't select any company
            st.write("Click on Search to Search for a Company")
            with st.spinner('Loading...'):
                time.sleep(1)
        else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data
# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here
elif selected == 'Stock Price Prediction':  # if user selects 'Stock Price Prediction'
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)
    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)
    dict_csv = pd.read_csv(r"Data.csv", header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list

    # Define the period for prediction
    period = st.sidebar.number_input('Forecast Period (days)', min_value=1, max_value=365, value=30)

    if a == "": 
        st.write("Enter a Stock Name")  
    else:  
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)  # reset index
        st.subheader('Raw Data of {}'.format(a))  # display raw data
        st.write(data)  # display data

        n_years = st.slider('Years of prediction:', 1, 4)
        period = n_years * 365  # number of days

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet() 
        m.fit(df_train)  

        future = m.make_future_dataframe(periods=period) 
        forecast = m.predict(future) 

        st.subheader('Forecast Data of {}'.format(a)) 
        st.write(forecast) 

        st.subheader(f'Forecast plot for {n_years} years') 
        fig1 = plot_plotly(m, forecast) 
        st.plotly_chart(fig1)  

        st.subheader("Forecast components of {}".format(a)) 
        fig2 = m.plot_components(forecast) 
        st.write(fig2) 

elif selected == 'About project':
    st.subheader("About")
    st.markdown("StockProject is an application that helps users to see Stock Price forecasting in Streamlit interface.")
