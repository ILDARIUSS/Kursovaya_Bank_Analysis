import pandas as pd
import logging

logger = logging.getLogger(__name__)

def generate_main_page(transactions, current_time):
    logger.info("🚀 Генерация главной страницы...")

    # Преобразуем столбец в datetime (с обработкой ошибок)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

    # Убираем строки с NaT (если не удалось распарсить дату)
    transactions = transactions.dropna(subset=["Дата операции"])

    # Преобразуем даты в ISO-формат для JSON
    transactions["Дата операции"] = transactions["Дата операции"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    start_date = pd.to_datetime(current_time).replace(day=1)

    # Фильтрация по дате
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date.strftime("%Y-%m-%dT%H:%M:%S")) &
        (transactions["Дата операции"] <= current_time)
    ]

    logger.info(f"📅 Фильтрация по датам: {start_date} - {current_time}")

    if filtered_transactions.empty:
        logger.warning("⚠️ Нет транзакций за выбранный период!")
        return {"greeting": "Доброе утро", "transactions": []}

    # Формируем JSON-ответ
    transactions_list = filtered_transactions.to_dict(orient="records")

    return {
        "greeting": "Доброе утро",
        "transactions": transactions_list
    }
