import datetime
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def process_transactions(transactions: List[Dict], month: int, year: int) -> List[Dict]:
    """Анализирует транзакции за указанный месяц и год.

    Args:
        transactions (List[Dict]): Список транзакций.
        month (int): Месяц анализа.
        year (int): Год анализа.

    Returns:
        List[Dict]: Отфильтрованный список транзакций.
    """
    filtered = [
        txn for txn in transactions
        if datetime.datetime.strptime(txn["Дата операции"], "%Y-%m-%dT%H:%M:%S").month == month and
           datetime.datetime.strptime(txn["Дата операции"], "%Y-%m-%dT%H:%M:%S").year == year
    ]

    logger.info(f"📅 Даты в файле: {transactions[0]['Дата операции']} - {transactions[-1]['Дата операции']}")
    if not filtered:
        logger.warning("⚠️ Нет транзакций за указанный период!")

    return filtered
