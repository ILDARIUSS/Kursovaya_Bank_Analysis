import pandas as pd
import logging

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_excel_transactions(filepath: str):
    """
    Читает данные о транзакциях из Excel-файла.
    :param filepath: Путь к файлу .xlsx
    :return: Список словарей с транзакциями
    """
    try:
        df = pd.read_excel(filepath, engine="openpyxl")
        transactions = df.to_dict(orient="records")  # Преобразуем в список словарей
        logging.info(f"Файл {filepath} успешно загружен. Найдено {len(transactions)} записей.")
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при загрузке {filepath}: {e}")
        return []
