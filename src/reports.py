import datetime
import logging
import pandas as pd
from functools import wraps

logger = logging.getLogger(__name__)

def log_execution(filename='default.json'):
    def inner(func):
        """Декоратор, логирующий выполнение функции."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_json(filename, force_ascii=False, indent=4)
            return result
        return wrapper
    return inner

@log_execution('my_report.json')
def generate_reports(transactions: pd.DataFrame, report_date: str = None) -> pd.DataFrame:
    """Генерирует отчет по тратам за последние 3 месяца.

    Args:
        transactions (pd.DataFrame): Датафрейм с транзакциями.
        report_date (str, optional): Дата отсчета (формат YYYY-MM-DD). Если не передана, используется текущая.

    Returns:
        pd.DataFrame: Средние траты по дням недели.
    """
    report_date = datetime.datetime.strptime(report_date, "%Y-%m-%d") if report_date else datetime.datetime.now()
    start_date = report_date - pd.DateOffset(months=3)

    logger.info(f"📊 Генерация отчёта с датой: {report_date.strftime('%Y-%m-%d')}")
    logger.info(f"📅 Выборка данных с {start_date.strftime('%Y-%m-%d')} по {report_date.strftime('%Y-%m-%d')}")

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors="coerce")
    filtered = transactions[(transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= report_date)]

    if filtered.empty:
        logger.warning("⚠️ Нет данных за выбранный период!")
        return pd.DataFrame(columns=["День недели", "Средние траты"])

    spending_by_weekday = filtered.groupby(filtered["Дата операции"].dt.day_name())["Сумма операции"].mean().reset_index()
    spending_by_weekday.columns = ["День недели", "Средние траты"]

    return spending_by_weekday


if __name__== '__main__':
    df = pd.read_excel('../data/operations.xlsx')
    generate_reports(df, '2021-11-13')