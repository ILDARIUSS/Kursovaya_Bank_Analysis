import pandas as pd
import logging
from src.utils import read_excel_transactions
from src.external_api import get_exchange_rate
import datetime

logger = logging.getLogger(__name__)


def generate_main_page(current_time: str):
    """
    Генерирует JSON-данные для главной страницы
    """
    logger.info("🚀 Генерация главной страницы...")

    # Загружаем транзакции
    transactions = read_excel_transactions("data/operations.xlsx")

    # Преобразуем дату в datetime
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

    # Определяем диапазон дат (последние 30 дней)
    target_date = pd.to_datetime(current_time)
    start_date = target_date - pd.Timedelta(days=30)

    logger.info("📅 Фильтрация по датам: %s - %s", start_date.date(), target_date.date())

    # Фильтруем транзакции за последние 30 дней
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= target_date)
        ]

    if filtered_transactions.empty:
        logger.warning("⚠️ Нет транзакций за последние 30 дней! Берём все данные.")
        filtered_transactions = transactions

    logger.info("✅ После фильтрации осталось записей: %d", len(filtered_transactions))

    # Группировка по картам
    financial_summary = (
        filtered_transactions.groupby("Номер карты")
        .agg({"Сумма операции": "sum", "Кэшбэк": "sum"})
        .reset_index()
    )

    financial_summary["Номер карты"] = financial_summary["Номер карты"].astype(str).str[-4:].apply(lambda x: f"*{x}")
    financial_summary = financial_summary.rename(columns={"Сумма операции": "total_spent", "Кэшбэк": "cashback"})

    logger.info("📊 Анализ кешбэка:\n%s", financial_summary.head(10))

    # 📌 **Новый отчёт: Траты по дням недели**
    filtered_transactions["День недели"] = filtered_transactions["Дата операции"].dt.day_name()
    spending_by_weekday = (
        filtered_transactions.groupby("День недели")["Сумма операции"].sum().round(2).to_dict()
    )

    logger.info("📅 Траты по дням недели:\n%s", spending_by_weekday)

    # Курс валют
    usd_rate = round(get_exchange_rate("USD"), 2)
    eur_rate = round(get_exchange_rate("EUR"), 2)

    # Финальный JSON-объект
    return {
        "greeting": "Доброе утро" if target_date.hour < 12 else "Добрый день",
        "cards": financial_summary.to_dict(orient="records"),
        "currency_rates": [
            {"currency": "USD", "rate": usd_rate},
            {"currency": "EUR", "rate": eur_rate},
        ],
        "reports": {  # 🔥 Добавляем отчёты сюда
            "spending_by_weekday": spending_by_weekday
        }
    }
