import datetime
import logging
import json
from utils import read_excel_transactions
from external_api import get_exchange_rate

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Пути к файлам
TRANSACTIONS_FILE = "data/operations.xlsx"

def get_financial_summary(transactions):
    """
    Генерирует сводку по финансам (сумма расходов и кешбэк) по последним 4 цифрам карт.
    """
    summary = {}

    for transaction in transactions:
        card = transaction.get("Номер карты", "")
        amount = transaction.get("Сумма платежа", 0)

        if not isinstance(card, str):
            card = str(card)

        last_digits = card[-4:] if len(card) >= 4 else "XXXX"

        # Игнорируем возвраты и нулевые платежи
        if amount <= 0:
            continue

        if last_digits not in summary:
            summary[last_digits] = {"total_spent": 0, "cashback": 0}

        summary[last_digits]["total_spent"] += amount
        summary[last_digits]["cashback"] += amount * 0.01  # 1% кешбэк

    return [
        {
            "last_digits": card if card != "XXXX" else "Неизвестная карта",
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2),
        }
        for card, data in summary.items()
    ]

def get_top_transactions(transactions, top_n=5):
    """
    Возвращает топ-N транзакций по сумме.
    """
    sorted_transactions = sorted(transactions, key=lambda x: x.get("Сумма платежа", 0), reverse=True)
    return [
        {
            "date": transaction.get("Дата платежа", "Неизвестно"),
            "amount": transaction.get("Сумма платежа", 0),
            "category": transaction.get("Категория", "Неизвестно"),
            "description": transaction.get("Описание", "Нет описания"),
        }
        for transaction in sorted_transactions[:top_n]
    ]

def get_currency_rates():
    """
    Получает текущие курсы валют (USD, EUR -> RUB).
    """
    currencies = ["USD", "EUR"]
    return [{"currency": cur, "rate": get_exchange_rate(cur)} for cur in currencies]

def get_stock_prices():
    """
    Заглушка для получения цен акций.
    """
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08},
    ]

def generate_main_page(date_str):
    """
    Формирует JSON-ответ для главной страницы.
    :param date_str: строка с датой и временем в формате "YYYY-MM-DD HH:MM:SS"
    :return: JSON-объект
    """
    now = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if 5 <= now.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= now.hour < 18:
        greeting = "Добрый день"
    elif 18 <= now.hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    transactions = read_excel_transactions(TRANSACTIONS_FILE)

    return json.dumps({
        "greeting": greeting,
        "cards": get_financial_summary(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
    }, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print(generate_main_page(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
