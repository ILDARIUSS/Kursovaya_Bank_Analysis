import datetime
import json
import requests
from collections import defaultdict
try:
    from src.external_api import get_exchange_rate
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.external_api import get_exchange_rate

API_STOCKS_URL = "https://api.apilayer.com/marketstack/v1/eod"  # Пример API для акций
API_KEY = "YOUR_ACCESS_KEY"  # Вставь свой API-ключ


def get_greeting():
    """Определяет время суток и возвращает приветствие"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def process_card_data(transactions):
    """Анализирует данные по картам: последние 4 цифры, расходы, кешбэк"""
    card_stats = defaultdict(lambda: {"total_spent": 0, "cashback": 0})

    for transaction in transactions:
        card_number = transaction.get("card_number", "")
        if len(card_number) >= 4:
            last_digits = card_number[-4:]
            amount_rub = transaction.get("amount_rub", 0)
            card_stats[last_digits]["total_spent"] += amount_rub
            card_stats[last_digits]["cashback"] = round(card_stats[last_digits]["total_spent"] * 0.01, 2)

    return [{"last_digits": card, **data} for card, data in card_stats.items()]


def get_top_transactions(transactions, n=5):
    """Выбирает топ-5 транзакций по сумме"""
    sorted_transactions = sorted(transactions, key=lambda x: x["amount_rub"], reverse=True)
    return sorted_transactions[:n]


def get_stock_prices():
    """Получает цены акций (пример запроса)"""
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    url = f"{API_STOCKS_URL}?access_key={API_KEY}&symbols={','.join(stocks)}"

    response = requests.get(url)
    data = response.json()

    if "data" in data:
        return [{"stock": item["symbol"], "price": item["close"]} for item in data["data"]]

    return []


def generate_main_page_data(transactions):
    """Формирует JSON-ответ для главной страницы"""
    return {
        "greeting": get_greeting(),
        "cards": process_card_data(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": [
            {"currency": "USD", "rate": get_exchange_rate("USD")},
            {"currency": "EUR", "rate": get_exchange_rate("EUR")}
        ],
        "stock_prices": get_stock_prices()
    }


# Пример использования
if __name__ == "__main__":
    transactions = [
        {"id": 1, "amount_rub": 9975.87, "card_number": "1234567890125814", "date": "2024-02-01"},
        {"id": 2, "amount_rub": 20588.33, "card_number": "1234567890127512", "date": "2024-02-02"},
        {"id": 3, "amount_rub": 5000.0, "card_number": "1234567890125814", "date": "2024-02-03"},
    ]

    result = generate_main_page_data(transactions)
    print(json.dumps(result, indent=4, ensure_ascii=False))  # Выводим красиво
