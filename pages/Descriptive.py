import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates

# from prophet import Prophet
# from prophet.diagnostics import performance_metrics
# from prophet.diagnostics import cross_validation
# from prophet.plot import plot_cross_validation_metric


def ts_plot(df):
    fig, ax = plt.subplots(figsize = (10,6) )
    
    half_year_locator = mdates.MonthLocator(interval=12)
    ax.set_facecolor('whitesmoke')
    ax.xaxis.set_major_locator(half_year_locator) # Locator for major axis only.
    # ax.scatter(df[df.sustained==1].Date, df[df.sustained==1].Level, s = 1, color = 'red')
    # sustained_dates = list(df[df.sustained==1].Date)
    # for sd in sustained_dates:
    #     ax.axvline(x=sd, color='darkgray', linestyle='-')
    # very_sustained_dates = list(df[df.very_sustained==1].Date)
    # for sd in very_sustained_dates:
    #     ax.axvline(x=sd, color='orange', linestyle='-')
    # exceptional_dates = list(df[df.exceptional==1].Date)
    # for sd in exceptional_dates:
    #     ax.axvline(x=sd, color='red', linestyle='-')
    ax.axhline(y=80, color = 'darkgray', linestyle = ':')
    ax.axhline(y=110, color = 'orange', linestyle = ':')
    ax.axhline(y=140, color = 'red', linestyle = ':')
    # ax.text(df.Date.min(),80,'Sustained level')
 
    ax.plot(df.Date, df.Level, color = 'black', linestyle = '-', lw = 1)
    return fig

def hist_plot(df):
    fig, ax = plt.subplots(figsize = (10,6) )
    
    ax.set_facecolor('whitesmoke')

    # count, bins = np.histogram(df.Level)
    data = pd.DataFrame(df[df.Level>80].groupby(df.Date.dt.year)['Level'].mean()).reset_index()

    ax.plot(data.Date, data.Level, color = 'black', linestyle = '-', lw = 1)
    return fig

st.set_page_config(page_title = 'Descriptive Statistics', layout="centered")
st.header ('Aqua Alta: Tides in Venice')
# st.image('./images/image.jpg')

tides = pd.read_csv('tides.csv')[['Date','Level']]

tides.Date = pd.to_datetime(tides.Date)

tides['sustained'] = tides.Level.apply(lambda x: 1 if (x>=80) and (x<110) else 0 )
tides['very_sustained'] = tides.Level.apply(lambda x: 1 if (x>=110) and (x<140) else 0 )
tides['exceptional'] = tides.Level.apply(lambda x: 1 if (x>=140) else 0 )

min_date = tides.Date.min().date()

max_date = tides.Date.max().date()
# min_date = dt.date (min_date)

    
st.markdown ('Select a date interval to update statistics')
date = st.slider('Make your Choice', min_value = min_date, value = (min_date, max_date), max_value = max_date)
# st.write(date[0])
# st.write(date[1])

# t_df = tides[(tides.Date>=pd.to_datetime(date[0])) & (tides.Date<=pd.to_datetime(date[1]))]

tides_daily = pd.DataFrame(tides[(tides.Date>=pd.to_datetime(date[0])) & (tides.Date<=pd.to_datetime(date[1]))].groupby(tides.Date.dt.date)['Level'].max()).reset_index()

tides_daily.Date = pd.to_datetime(tides_daily.Date)
# st.write(tides.columns)
# st.write(date)

tides_daily['sustained'] = tides_daily.Level.apply(lambda x: 1 if (x>=80) and (x<110) else 0 )
tides_daily['very_sustained'] = tides_daily.Level.apply(lambda x: 1 if (x>=110) and (x<140) else 0 )
tides_daily['exceptional'] = tides_daily.Level.apply(lambda x: 1 if (x>=140) else 0 )

sustained = tides_daily.sustained.sum()
very_sustained = tides_daily.very_sustained.sum()
exceptional = tides_daily.exceptional.sum()

message = 'In the period from **' + date[0].strftime('%B %d, %Y') + '** and **' + date[1].strftime('%B %d, %Y') + '** Venezia has seen ' 

if sustained > 0:
    message += ' **' + str(sustained) + '** days of sustained tide, '
else:
    message += 'no days of sustained tide, '

if very_sustained > 0 :
    message += '**' + str(very_sustained) + '** days of very sustained tide, '
else:
    message += 'no days of very sustained tide, '

if exceptional > 0 :
    message += 'and **' + str(exceptional) + '** days of exceptional tide '
else:
    message += 'no days of exceptional tide'

st.markdown(message)

st.pyplot(ts_plot(tides_daily))
st.caption('Max value of sea level on a daily basis')

st.pyplot(hist_plot(tides_daily))
st.caption('Sea Level Average, when sea level is higher than 80 cm')


