import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates




def ts_plot(df):
    fig, ax = plt.subplots(figsize = (12,6) )
    
    half_year_locator = mdates.MonthLocator(interval=12)
    ax.set_facecolor('whitesmoke')
    ax.xaxis.set_major_locator(half_year_locator) # Locator for major axis only.

    ax.axhline(y=80, color = 'darkgray', linestyle = ':')
    ax.axhline(y=110, color = 'orange', linestyle = ':')
    ax.axhline(y=140, color = 'red', linestyle = ':')
 
    ax.plot(df.Date, df.Level, color = 'black', linestyle = '-', lw = 1)
    return fig

def hist_plot(df):
    fig, ax = plt.subplots(3,1, figsize = (12,6) )


    data = df

    ax[0].set_facecolor('whitesmoke')
    ax[0].set_title('Number of Sustained tide hours per months')
    p = ax[0].bar(data.mn, data.sustained, color='darkgrey')
    ax[0].bar_label(p, label_type='center', padding= 6)

    ax[1].set_facecolor('whitesmoke')
    ax[1].set_title('Number of Very Sustained tide hours per months')
    p=ax[1].bar(data.mn, data.very_sustained, color='orange')
    ax[1].bar_label(p, label_type='center', padding= 6)

    ax[2].set_facecolor('whitesmoke')
    ax[2].set_title('Number of Exceptional tide hours per months')
    p=ax[2].bar(data.mn, data.exceptional, color='red')
    ax[2].bar_label(p, label_type='center', padding= 6)

    fig.tight_layout()
    return fig

st.set_page_config(page_title = 'Descriptive Statistics', layout="centered")
st.header ('Aqua Alta: Tides in Venice')

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
    message += ' **' + str(sustained) + '** days when tides were **sustained**, '
else:
    message += 'no days of sustained tide, '

if very_sustained > 0 :
    message += '**' + str(very_sustained) + '** days when tides were **very sustained**, '
else:
    message += 'no days of very sustained tide, '

if exceptional > 0 :
    message += 'and **' + str(exceptional) + '** days where tides were **exceptional**'
else:
    message += 'no days of exceptional tide'

st.markdown(message)

st.pyplot(ts_plot(tides_daily))
st.caption('Max value of sea level on a daily basis')


t_y = pd.DataFrame(tides[(tides.Date>=pd.to_datetime(date[0])) & (tides.Date<=pd.to_datetime(date[1]))]).groupby(tides.Date.dt.month)['sustained','very_sustained','exceptional'].sum().reset_index()
# t_y = tides.groupby(tides.Date.dt.month)['sustained','very_sustained','exceptional'].sum().reset_index()
t_y['mn']=t_y.Date.apply(lambda x: dt.date(1900, x, 1).strftime('%b'))

st.pyplot(hist_plot(t_y))
st.caption('Distribution of tide severe events by month')


