import pandas as pd
import logging

logger = logging.getLogger(__name__)

def process_transactions(transactions, month, year):
    logger.info(f"📊 Анализ транзакций за {month:02d}-{year}")

    # Проверяем, что даты в правильном формате
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")

    # Убираем NaT
    transactions = transactions.dropna(subset=["Дата операции"])

    # Выбираем транзакции за указанный месяц и год
    filtered_transactions = transactions[
        (transactions["Дата операции"].dt.month == month) &
        (transactions["Дата операции"].dt.year == year)
    ]

    # Логируем диапазон дат в файле
    min_date = transactions["Дата операции"].min().strftime("%Y-%m-%dT%H:%M:%S")
    max_date = transactions["Дата операции"].max().strftime("%Y-%m-%dT%H:%M:%S")
    logger.info(f"📅 Даты в файле: {min_date} - {max_date}")

    if filtered_transactions.empty:
        logger.warning("⚠️ Нет транзакций за указанный период!")
        return {"transactions": []}

    # Конвертируем даты в JSON-совместимый формат
    filtered_transactions.loc[:, "Дата операции"] = filtered_transactions["Дата операции"].dt.strftime(
        "%Y-%m-%dT%H:%M:%S")

    return {
        "transactions": filtered_transactions.to_dict(orient="records")
    }
