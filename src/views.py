import pandas as pd
import datetime
import logging
from src.utils import read_excel_transactions
from src.external_api import get_exchange_rate

logger = logging.getLogger(__name__)

def generate_main_page(current_time):
    logger.info("🚀 Генерация главной страницы...")

    # Читаем данные
    transactions = read_excel_transactions("data/operations.xlsx")

    # Преобразуем дату операции в datetime, добавляем `dayfirst=True`
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True, errors="coerce"
    )

    # Определяем диапазон дат (последние 30 дней)
    target_date = datetime.date.today()
    start_date = target_date - datetime.timedelta(days=30)
    logger.info("📅 Фильтрация по датам: %s - %s", start_date, target_date)

    # Фильтруем транзакции за последние 30 дней
    recent_transactions = transactions[
        (transactions["Дата операции"].dt.date >= start_date) &
        (transactions["Дата операции"].dt.date <= target_date)
    ]

    if recent_transactions.empty:
        logger.warning("⚠️ Нет транзакций за последние 30 дней! Берём все данные.")
        recent_transactions = transactions

    logger.info("✅ После фильтрации осталось записей: %d", len(recent_transactions))

    # Анализ кешбэка
    cashback_summary = recent_transactions.groupby("Номер карты").agg(
        total_spent=pd.NamedAgg(column="Сумма операции", aggfunc="sum"),
        cashback=pd.NamedAgg(column="Кэшбэк", aggfunc="sum")
    ).reset_index()

    cashback_summary["cashback"] = cashback_summary["cashback"].fillna(0).round(2)
    logger.info("📊 Анализ кешбэка:\n%s", cashback_summary)

    # Анализ трат по дням недели
    transactions["День недели"] = transactions["Дата операции"].dt.day_name()
    spending_by_weekday = transactions.groupby("День недели")["Сумма операции"].sum().to_dict()
    logger.info("📅 Траты по дням недели:\n%s", spending_by_weekday)

    # Получаем курсы валют
    currency_rates = [
        {"currency": "USD", "rate": get_exchange_rate("USD")},
        {"currency": "EUR", "rate": get_exchange_rate("EUR")}
    ]
    logger.info("💰 Курс валют: %s", currency_rates)

    return {
        "greeting": "Доброе утро",
        "cards": cashback_summary.to_dict(orient="records"),
        "currency_rates": currency_rates,
        "reports": {
            "spending_by_weekday": spending_by_weekday
        }
    }
