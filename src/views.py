import pandas as pd
import json
import datetime
import logging
from src.utils import read_excel_transactions
from src.external_api import get_exchange_rate

# Настраиваем логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_financial_summary(transactions: pd.DataFrame):
    """
    Генерирует список данных о картах (последние 4 цифры, общая сумма трат, кешбэк).
    """
    summary = transactions.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"}).reset_index()

    # Обрабатываем пустые значения
    summary["Номер карты"] = summary["Номер карты"].fillna("Неизвестная карта")  # Заменяем NaN
    summary["last_digits"] = summary["Номер карты"].astype(str).str[-4:]  # Берём последние 4 цифры
    summary["cashback"] = summary["Кэшбэк"].fillna(0).round(2)  # Убеждаемся, что кешбэк не NaN

    logger.info("📊 Анализ кешбэка:\n%s", summary[["Номер карты", "Сумма операции", "Кэшбэк"]].head(10))

    return summary[["last_digits", "Сумма операции", "cashback"]].rename(
        columns={"Сумма операции": "total_spent"}
    ).to_dict(orient="records")

def generate_main_page(current_datetime: str):
    """
    Генерирует JSON-ответ для главной страницы.
    """
    transactions = read_excel_transactions("data/operations.xlsx")

    # Получаем курс валют
    usd_rate = get_exchange_rate("USD")
    eur_rate = get_exchange_rate("EUR")

    # Приветствие в зависимости от времени суток
    hour = datetime.datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S").hour
    if hour < 6:
        greeting = "Доброй ночи"
    elif hour < 12:
        greeting = "Доброе утро"
    elif hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    return json.dumps({
        "greeting": greeting,
        "cards": get_financial_summary(transactions),
        "top_transactions": transactions.nlargest(5, "Сумма операции")[["Дата операции", "Сумма операции", "Категория", "Описание"]].rename(
            columns={"Дата операции": "date", "Сумма операции": "amount", "Категория": "category", "Описание": "description"}
        ).to_dict(orient="records"),
        "currency_rates": [{"currency": "USD", "rate": usd_rate}, {"currency": "EUR", "rate": eur_rate}]
    }, ensure_ascii=False, indent=4)
