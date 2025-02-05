import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)

def log_execution_time(func):
    """Декоратор для логирования времени выполнения функции."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.info(f"⏳ Время выполнения {func.__name__}: {elapsed_time:.4f} сек")
        return result
    return wrapper

@log_execution_time
def generate_reports(transactions: pd.DataFrame):
    """Генерирует отчёт о тратах по дням недели."""
    if transactions.empty:
        logging.warning("⚠️ Нет данных для генерации отчёта!")
        return {}

    transactions["День недели"] = transactions["Дата операции"].dt.day_name()
    spending_by_weekday = transactions.groupby("День недели")["Сумма операции"].sum().to_dict()

    logging.info(f"📅 Траты по дням недели:\n{spending_by_weekday}")
    return {"spending_by_weekday": spending_by_weekday}
