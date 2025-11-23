import pandas as pd




def transform_weather_current(raw: dict) -> pd.DataFrame:
    """
    Transform current weather API response into a clean DataFrame.
    """
    try:
        df = pd.DataFrame([{
            "city": raw.get("name"),
            "temp": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"],
            "pressure": raw["main"]["pressure"],
            "description": raw["weather"][0]["description"],
            "wind_speed": raw["wind"]["speed"]
        }])
        return df
    
    except Exception as e:
        raise ValueError(f"Error transforming current weather data: {e}")



def transform_weather_forecast(raw: dict) -> pd.DataFrame:
    """
    Transform 5-day weather forecast API response into a clean DataFrame.
    """
    try:
        records = []
        for item in raw["list"]:
            records.append({
                "datetime": item["dt_txt"],
                "temp": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "description": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"]
            })

        df = pd.DataFrame(records)
        df["datetime"] = pd.to_datetime(df["datetime"])

        return df

    except Exception as e:
        raise ValueError(f"Error transforming forecast weather data: {e}")
