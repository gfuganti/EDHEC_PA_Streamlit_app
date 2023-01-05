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

try:
    from matplotlib import pyplot as plt
    from matplotlib.dates import (
        MonthLocator,
        num2date,
        AutoDateLocator,
        AutoDateFormatter,
    )
except ImportError:
    logger.error('Importing matplotlib failed. Plotting will not work.')


def model_fit(df):
    with st.spinner ('Fitting Model'):

        m = Prophet( seasonality_mode='additive', \
            changepoint_prior_scale=0.01, \
                    yearly_seasonality=10, \
                    weekly_seasonality=False, daily_seasonality=True)
        m.add_seasonality(name='lunar', period = 29.53, fourier_order = 5)

        m.fit(df[(df.ds>=pd.to_datetime(date[0])) & (df.ds<=pd.to_datetime(date[1]))])

    with st.spinner('Forecasting'):

        future = m.make_future_dataframe(periods = 72, freq = 'H')

        forecast = m.predict(future)
    return m, forecast


def gf_plot(
    m, fcst, ax=None, uncertainty=True, plot_cap=True, xlabel='ds', ylabel='y',
    figsize=(10, 6), include_legend=False, tail = 0, future = 0
):
    """Plot the Prophet forecast.
    Parameters
    ----------
    m: Prophet model.
    fcst: pd.DataFrame output of m.predict.
    ax: Optional matplotlib axes on which to plot.
    uncertainty: Optional boolean to plot uncertainty intervals, which will
        only be done if m.uncertainty_samples > 0.
    plot_cap: Optional boolean indicating if the capacity should be shown
        in the figure, if available.
    xlabel: Optional label name on X-axis
    ylabel: Optional label name on Y-axis
    figsize: Optional tuple width, height in inches.
    include_legend: Optional boolean to add legend to the plot.
    Returns
    -------
    A matplotlib figure.
    """
    if ax is None:
        fig = plt.figure(facecolor='w', figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        fig = ax.get_figure()
    fcst_t = fcst['ds'].dt.to_pydatetime()

    if tail ==0:
        ax.plot(m.history['ds'].dt.to_pydatetime(), m.history['y'], 'k.',
                label='Observed data points')
        ax.plot(fcst_t, fcst['yhat'], ls='-', c='#0072B2', label='Forecast')
        if 'cap' in fcst and plot_cap:
            ax.plot(fcst_t, fcst['cap'], ls='--', c='k', label='Maximum capacity')
        if m.logistic_floor and 'floor' in fcst and plot_cap:
            ax.plot(fcst_t, fcst['floor'], ls='--', c='k', label='Minimum capacity')
        if uncertainty and m.uncertainty_samples:
            ax.fill_between(fcst_t, fcst['yhat_lower'], fcst['yhat_upper'],
                            color='#0072B2', alpha=0.2, label='Uncertainty interval')
        # Specify formatting to workaround matplotlib issue #12925
        locator = AutoDateLocator(interval_multiples=False)
        formatter = AutoDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)

    else:

        hh = m.history.iloc[-tail:]
        ff = fcst.iloc[-tail-future:]
        fcst_t = ff['ds'].dt.to_pydatetime()

        ax.plot(hh['ds'].dt.to_pydatetime(), hh['y'], 'k.',
                label='Observed data points')
        ax.plot(fcst_t, ff['yhat'], ls='-', c='#0072B2', label='Forecast')

        if 'cap' in fcst and plot_cap:
            ax.plot(fcst_t, ff['cap'], ls='--', c='k', label='Maximum capacity')
        if m.logistic_floor and 'floor' in fcst and plot_cap:
            ax.plot(fcst_t, ff['floor'], ls='--', c='k', label='Minimum capacity')
        if uncertainty and m.uncertainty_samples:
            ax.fill_between(fcst_t, ff['yhat_lower'], ff['yhat_upper'],
                            color='#0072B2', alpha=0.2, label='Uncertainty interval')
        # Specify formatting to workaround matplotlib issue #12925
        locator = AutoDateLocator(interval_multiples=False)
        formatter = AutoDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)


    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if include_legend:
        ax.legend()
    fig.tight_layout()
    return fig


tides = pd.read_csv('tides.csv')[['Date','Level']]

tides.Date = pd.to_datetime(tides.Date)

min_date = tides.Date.min().date()

max_date = tides.Date.max().date()


tides.rename(columns={'Date':'ds', 'Level':'y'}, inplace = True)

st.markdown ('Select a date interval to update statistics')
date = st.slider('Make your Choice', min_value = min_date, value = (min_date, max_date), max_value = max_date)

if st.button ("Run"):
    m, forecast = model_fit(tides)
    st.pyplot(gf_plot(m, forecast, tail = 24*30, future = 70, include_legend = True))


