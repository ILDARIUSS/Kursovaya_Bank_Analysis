import datetime
import json
import logging
import os

import pandas as pd
import requests
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_EXCHANGE_RATES = "https://api.apilayer.com/exchangerates_data/latest"
API_STOCK_PRICES = "https://finnhub.io/api/v1/quote"


def get_greeting(current_time: datetime.datetime) -> str:
    """Возвращает приветствие в зависимости от текущего времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def fetch_exchange_rates(currencies: List[str]) -> List[Dict]:
    """Получает курсы валют к рублю."""
    api_key = os.getenv('API_EXCHANGE_RATES_KEY')
    headers = {"apikey": api_key}

    result = []
    for currency in currencies:
        params = {"base": currency, "symbols": "RUB"}

        response = requests.get(API_EXCHANGE_RATES, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            result.append({"currency": currency, "rate": data["rates"].get("RUB", None)})
        else:
            logger.warning(f"Ошибка при получении курсов валют: {response.status_code}")
            return []
    return result


def fetch_stock_prices(stocks: List[str]) -> List[Dict]:
    """Получает стоимость акций."""
    api_key = os.getenv('API_STOCK_PRICES_KEY')
    stock_prices = []

    for stock in stocks:
        params = {"symbol": stock, "token": api_key}
        response = requests.get(API_STOCK_PRICES, params=params)
        if response.status_code == 200:
            data = response.json()
            stock_prices.append({"stock": stock, "price": data.get("c", None)})
        else:
            logger.warning(f"Ошибка при получении цены акции {stock}: {response.status_code}")

    return stock_prices


def generate_main_page(transactions: pd.DataFrame, current_time: str) -> Dict:
    """Генерирует данные для главной страницы."""
    current_time = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    start_date = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= current_time)
        ]

    if filtered_transactions.empty:
        logger.warning("⚠️ Нет транзакций за выбранный период!")
        return {"greeting": get_greeting(current_time), "transactions": []}

    expenses_only = filtered_transactions[filtered_transactions['Сумма операции'] < 0]
    # Анализ трат по картам
    cards_summary = expenses_only.groupby("Номер карты").agg(
        total_spent=pd.NamedAgg(column="Сумма операции", aggfunc="sum"),
        cashback=pd.NamedAgg(column="Сумма операции", aggfunc=lambda x: round(abs(x.sum()) * 0.01, 2))
    ).reset_index()

    cards_summary["Номер карты"] = cards_summary["Номер карты"].astype(str).str[-4:]

    cards = cards_summary.to_dict(orient="records")

    # Топ-5 транзакций по сумме платежа
    top_transactions = filtered_transactions.nlargest(5, "Сумма операции")[
        ["Дата операции", "Сумма операции", "Категория", "Описание"]]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    top_transactions.rename(columns={"Дата операции": "date", "Сумма операции": "amount", "Категория": "category",
                                     "Описание": "description"}, inplace=True)
    top_transactions = top_transactions.to_dict(orient="records")

    # Загрузка user_settings.json
    try:
        with open("src/user_settings.json", "r", encoding="utf-8") as file:
            user_settings = json.load(file)
        currencies = user_settings.get("user_currencies", [])
        stocks = user_settings.get("user_stocks", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"⚠️ Ошибка при загрузке user_settings.json: {e}")
        currencies, stocks = [], []

    # Получение курсов валют и цен акций
    currency_rates = fetch_exchange_rates(currencies) if currencies else []
    stock_prices = fetch_stock_prices(stocks) if stocks else []

    now_moment = datetime.datetime.now()

    return {
        "greeting": get_greeting(now_moment),
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
