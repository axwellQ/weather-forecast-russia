import requests
import json

API_KEY = "add7c47f139d402e0d395d874149dfef"  # Твой ключ
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_forecast(city: str):
    """Получение прогноза погоды по городу"""
    params = {
        "q": city + ",RU",  # Ограничиваем поиск Россией
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return {"Ошибка": data.get("message", "Не удалось получить данные")}

        # Вывод первых 10 прогнозов (каждые 3 часа)
        forecast_list = []
        for item in data["list"][:10]:
            forecast_list.append({
                "Дата и время": item["dt_txt"],
                "Температура (°C)": item["main"]["temp"],
                "Ощущается (°C)": item["main"]["feels_like"],
                "Влажность (%)": item["main"]["humidity"],
                "Погода": item["weather"][0]["description"]
            })
        return forecast_list

    except requests.RequestException as e:
        return {"Ошибка": str(e)}


def main():
    print("=== Прогноз погоды по городам России ===")
    while True:
        city = input("\nВведите город (или 'выход' для выхода): ").strip()
        if city.lower() == "выход":
            print("До встречи!")
            break

        forecast = get_forecast(city)
        if isinstance(forecast, dict) and "Ошибка" in forecast:
            print("❌", forecast["Ошибка"])
        else:
            print(f"\nПрогноз для {city}:")
            for item in forecast:
                print(f"{item['Дата и время']} | {item['Температура (°C)']}°C | "
                      f"{item['Ощущается (°C)']}°C | {item['Влажность (%)']}% | {item['Погода']}")
def get_current_forecast(city: str):
    params = {"q": city + ",RU", "appid": API_KEY, "units": "metric", "lang": "ru"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return {"Ошибка": data.get("message", "Не удалось получить данные")}

    # Берём первый ближайший прогноз
    item = data["list"][0]
    return {
        "Город": data["city"]["name"],
        "Дата и время": item["dt_txt"],
        "Температура (°C)": item["main"]["temp"],
        "Ощущается (°C)": item["main"]["feels_like"],
        "Влажность (%)": item["main"]["humidity"],
        "Погода": item["weather"][0]["description"]
    }


if __name__ == "__main__":
    main()
