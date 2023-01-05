import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates

from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric


def ts_plot(df):
    fig, ax = plt.subplots(figsize = (10,6) )
    
    half_year_locator = mdates.MonthLocator(interval=12)
    ax.set_facecolor('whitesmoke')
    ax.xaxis.set_major_locator(half_year_locator) # Locator for major axis only.
    # ax.scatter(df[df.sustained==1].Date, df[df.sustained==1].Level, s = 1, color = 'red')
    sustained_dates = list(df[df.sustained==1].Date)
    for sd in sustained_dates:
        ax.axvline(x=sd, color='darkgray', linestyle='-')
    very_sustained_dates = list(df[df.very_sustained==1].Date)
    for sd in very_sustained_dates:
        ax.axvline(x=sd, color='orange', linestyle='-')
    exceptional_dates = list(df[df.exceptional==1].Date)
    for sd in exceptional_dates:
        ax.axvline(x=sd, color='red', linestyle='-')
 
    ax.plot(df.Date, df.Level, color = 'black', linestyle = '-', lw = 1)
    return fig


st.set_page_config(page_title='Home', layout="centered")
st.header ('Aqua Alta: Tides in Venice')
st.image('./images/image.jpg')

tides = pd.read_csv('tides.csv')[['Date','Level']]

tides.Date = pd.to_datetime(tides.Date)

tides['sustained'] = tides.Level.apply(lambda x: 1 if (x>=80) and (x<110) else 0 )
tides['very_sustained'] = tides.Level.apply(lambda x: 1 if (x>=110) and (x<140) else 0 )
tides['exceptional'] = tides.Level.apply(lambda x: 1 if (x>=140) else 0 )

min_date = tides.Date.min().date()

max_date = tides.Date.max().date()
# min_date = dt.date (min_date)



st.write ('Starting from Autumn until the beginning of Spring, the phenomenon of high water is quite frequent in Venice.')
# st.write('And yet, the high tide does not bathe the Calli and Campi of Venice in the same way in all areas. <br> While Piazza San Marco is covered by several centimeters of water it is probable that other areas of the historic center are completely dry.')
st.write('However, to be more precise, we speak of high water only when the height of the water exceeds a certain level.')
st.write('The zero tide point of Punta della Salute is taken as a reference point.')
st.write('Considering that the average height of Venice is about 1 metre, the tide is defined as:')
st.markdown('- **sustained** when it is between 80 and 109 cm' )
st.markdown('- **very sustained** when it is between 110 and 139 centimetres')
st.markdown('- **exceptional** when it exceeds 140 centimeters and therefore the water floods 59 percent of the city')
# st.write('. Fortunately, the latter case study is quite sporadic.'\
#     'In any case, even if a particularly high tide is expected on a particular day, it must always be considered that the peaks are present only in certain hours of the day.'\
#     'We want to see how to understand when high tide is actually expected in Venice?'\
#     'When high water occurs: Here\'s the mix of conditions'\
#     'high water in the city'\
#     'One of the most important floods was that of November 4, 1966. In this photo, the Ponte della Paglia, next to Palazzo Ducale (photo by https://garystockbridge617.getarchive.net/ - public domain)'\
#     'To arrive at the occurrence of high water, some specific meteorological and astronomical conditions must be verified.'\
#     'In fact, high water occurs again in the coldest months coinciding with the sirocco wind which prevents the water from flowing normally and pushes large masses from south to north. Sometimes the phenomenon occurs even when it\'s hotter and even in summer, but the water levels are usually quite low.'\
#     'Lately, due to global warming and climate change, the phenomena are becoming more intense and destructive (not only in Venice). In support of the city, however, there is the Mose, a system of mobile dams that protect the city from the most intense tides).'\
#     'Normally, when it is expected, the water rises for six hours and then decreases for the same period of time. The peaks are more limited in time, lasting for about 3 to 4 hours in the waxing phase.')
st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)




st.table(tides.groupby(tides.Date.dt.year)['sustained','very_sustained','exceptional'].sum().reset_index().set_index('Date').rename(columns = {'very_sustained':'very sustained'}))
st.caption('No. of days of high tides from 2011 to 2021')
st.caption('Data elaborated from https://dati.venezia.it/?q=content/cpsm-dati-meteomarini-laguna-e-litorale-veneziano')

