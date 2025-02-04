import pandas as pd
import datetime
import logging
from src.utils import read_excel_transactions
from src.external_api import get_exchange_rate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_financial_summary(transactions):
    """Группировка транзакций по картам."""
    if transactions.empty:
        logger.warning("⚠️ Нет данных для анализа транзакций!")
        return []

    summary = transactions.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"}).reset_index()

    summary["total_spent"] = summary["Сумма операции"].fillna(0).round(2)
    summary["cashback"] = summary["Кэшбэк"].fillna(0).round(2)
    summary["last_digits"] = summary["Номер карты"].astype(str).str[-4:]

    logger.info("📊 Анализ кешбэка:\n%s", summary[["Номер карты", "Сумма операции", "Кэшбэк"]].head(10))

    return summary[["last_digits", "total_spent", "cashback"]].to_dict(orient="records")


def generate_main_page(current_time):
    """Генерация JSON-структуры главной страницы."""
    logger.info("🚀 Генерация главной страницы...")

    transactions = read_excel_transactions("data/operations.xlsx")

    if transactions.empty:
        logger.warning("⚠️ Нет данных для анализа!")
        return {"greeting": "Нет данных", "cards": [], "top_transactions": [], "currency_rates": []}

    # Преобразуем даты
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S",
                                                   errors="coerce")

    target_date = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").date()
    start_date = target_date - datetime.timedelta(days=30)

    logger.info(f"📅 Фильтрация по датам: {start_date} - {target_date}")

    filtered_transactions = transactions[
        (transactions["Дата операции"].dt.date >= start_date) &
        (transactions["Дата операции"].dt.date <= target_date)
        ]

    if filtered_transactions.empty:
        logger.warning("⚠️ Нет транзакций за последние 30 дней! Берём все данные.")
        filtered_transactions = transactions

    logger.info(f"✅ После фильтрации осталось записей: {len(filtered_transactions)}")

    cards_summary = get_financial_summary(filtered_transactions)

    # Преобразуем дату в строку
    top_transactions = filtered_transactions.nlargest(5, "Сумма операции")[
        ["Дата операции", "Сумма операции", "Категория", "Описание"]
    ]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%Y-%m-%d %H:%M:%S")

    top_transactions = top_transactions.rename(
        columns={"Дата операции": "date", "Сумма операции": "amount", "Категория": "category",
                 "Описание": "description"}).to_dict(orient="records")

    usd_rate = get_exchange_rate("USD")
    eur_rate = get_exchange_rate("EUR")

    return {
        "greeting": "Доброе утро",
        "cards": cards_summary,
        "top_transactions": top_transactions,
        "currency_rates": [
            {"currency": "USD", "rate": round(usd_rate, 2)},
            {"currency": "EUR", "rate": round(eur_rate, 2)}
        ]
    }
