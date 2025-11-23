import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd


# Local imports
from api_client.weather_api import (
    get_forecast_5day_by_city,
    get_current_weather_by_city,
    WeatherAPIError
)
from etl.extract import load_cache, save_cache, cache_key

from etl.transform import (
    transform_weather_forecast,
    transform_weather_current
)

from analysis.plots import (
    plot_weather_timeseries,
    plot_weather_humidity
)

load_dotenv()

st.set_page_config(page_title='Weather ETL Dashboard', layout='wide')

st.title('Weather ETL + Real-time Dashboard')

# --- Sidebar ---
city = st.sidebar.text_input('City', value='Lahore')
which = st.sidebar.radio('Choose Data', ['Current', '5-day Forecast'])
CACHE_TTL = st.sidebar.number_input('Cache TTL (seconds)', value=600, min_value=60)

# --- Main Logic ---
try:
    key = cache_key('weather', f"{city}_{which}")
    cached = load_cache(key, max_age_seconds=CACHE_TTL)

    if cached is None:
        # Fetch new API data
        if which == 'Current':
            raw = get_current_weather_by_city(city)
            df = transform_weather_current(raw)
        else:
            raw = get_forecast_5day_by_city(city)
            df = transform_weather_forecast(raw)

        # Save to cache
        save_cache(key, df)

    else:
        # Load from cache
        df = cached

    st.success("Data loaded successfully!")

    st.dataframe(df)

    # --- Plots ---
    if which == '5-day Forecast':
        st.plotly_chart(plot_weather_timeseries(df), use_container_width=True)
        st.plotly_chart(plot_weather_humidity(df), use_container_width=True)

    else:
        st.write("Current weather does not include timeseries plots.")

except WeatherAPIError as e:
    st.error(f"API Error: {e}")

except Exception as e:
    st.error(f"Unexpected Error: {e}")
