import requests
import json

API_KEY = "Q2Q5KznEkjKACyQwlNdeb1nptrGML5wu"  # Замени на свой API-ключ
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(currency: str) -> float:
    """Получает курс валюты по отношению к рублю (RUB)"""
    url = f"{BASE_URL}?base={currency}&symbols=RUB"
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200 or "error" in data:
        raise ValueError(f"Ошибка при получении курса: {data}")

    rate = data["rates"].get("RUB")
    if rate is None:
        raise ValueError(f"Не удалось получить курс для {currency}")

    return rate


def convert_transactions_to_rub(transactions):
    """Конвертирует суммы транзакций в рубли"""
    converted_transactions = []

    for transaction in transactions:
        amount = transaction["amount"]
        currency = transaction["currency"]

        if currency != "RUB":
            exchange_rate = get_exchange_rate(currency)
            amount *= exchange_rate  # Пересчитываем в рубли

        transaction["amount_rub"] = round(amount, 2)  # Добавляем пересчитанную сумму
        converted_transactions.append(transaction)

    return converted_transactions


# Пример использования
transactions = [
    {"id": 1, "amount": 100.0, "currency": "USD", "date": "2024-02-01"},
    {"id": 2, "amount": 200.0, "currency": "EUR", "date": "2024-02-02"},
    {"id": 3, "amount": 5000.0, "currency": "RUB", "date": "2024-02-03"}
]

converted = convert_transactions_to_rub(transactions)
print(json.dumps(converted, indent=4, ensure_ascii=False))  # Выводим результат красиво
