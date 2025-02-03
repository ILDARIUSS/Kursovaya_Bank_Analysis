import os
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения из .env
load_dotenv()

def get_exchange_rate(currency: str) -> float:
    """Получает курс валюты к рублю с API."""
    API_KEY = os.getenv("EXCHANGE_API_KEY")  # Берём ключ из окружения
    if not API_KEY:
        raise ValueError("Ошибка: API-ключ не найден!")

    URL = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
    headers = {"apikey": API_KEY}

    response = requests.get(URL, headers=headers)
    data = response.json()

    if not data.get("success"):
        raise ValueError(f"Не удалось получить курс для {currency}. Ответ API: {data}")

    return data["rates"]["RUB"]
