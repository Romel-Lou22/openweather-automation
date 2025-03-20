import requests
import pandas as pd
import os
from datetime import datetime

# Parámetros de OpenWeather (endpoint /weather gratuito)
lat = "-1.34627"
lon = "-78.66877"
api_key = "f3cf409a368f5d9b5ffbd8049bcfd53b"
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric"
}

def get_weather_data():
    """Consulta la API y retorna un registro con la fecha, temperatura y humedad."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        main = data.get("main", {})
        temp = main.get("temp")
        humidity = main.get("humidity")
        now = datetime.utcnow()  # Hora actual en UTC
        return {"datetime": now, "temperature": temp, "humidity": humidity}
    else:
        print("Error en la consulta:", response.status_code)
        return None

def update_local_csv(record, filename="openweather_data.csv"):
    """Agrega el registro al CSV; si no existe, lo crea."""
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename, parse_dates=["datetime"])
        df_new = pd.DataFrame([record])
        df_total = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_total = pd.DataFrame([record])
    df_total.to_csv(filename, index=False)
    print(f"Datos actualizados en {filename}")

if __name__ == "__main__":
    record = get_weather_data()
    if record:
        update_local_csv(record)
