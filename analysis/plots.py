import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def _ensure_datetime(df: pd.DataFrame, col: str = 'dt') -> pd.DataFrame:
    df = df.copy()
    if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col])
    return df


def plot_weather_timeseries(df: pd.DataFrame) -> go.Figure:
    df = _ensure_datetime(df, 'dt')
    fig = px.line(df, x='dt', y='temp_c', title='Temperature (°C) over time',
                  labels={'temp_c': 'Temp (°C)', 'dt': 'DateTime'})
    return fig


def plot_weather_humidity(df: pd.DataFrame) -> go.Figure:
    df = _ensure_datetime(df, 'dt')
    fig = px.line(df, x='dt', y='humidity', title='Humidity over time',
                  labels={'humidity': 'Humidity', 'dt': 'DateTime'})
    return fig


def plot_stock_line(df: pd.DataFrame) -> go.Figure:
    df = _ensure_datetime(df, 'dt')
    fig = px.line(df, x='dt', y='close', title='Closing Price',
                  labels={'close': 'Close', 'dt': 'DateTime'})
    return fig


def plot_candlestick(df: pd.DataFrame) -> go.Figure:
    df = _ensure_datetime(df, 'dt')
    fig = go.Figure(data=[go.Candlestick(x=df['dt'], open=df['open'],
                                         high=df['high'], low=df['low'], close=df['close'])])
    fig.update_layout(title='Candlestick')
    return fig


def plot_volume(df: pd.DataFrame) -> go.Figure:
    df = _ensure_datetime(df, 'dt')
    fig = px.bar(df, x='dt', y='volume', title='Volume')
    return fig
