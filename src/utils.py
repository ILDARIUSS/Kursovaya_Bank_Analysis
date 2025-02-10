import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_transactions(filepath: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла и приводит данные к нужному формату.

    :param filepath: Путь к файлу Excel.
    :return: DataFrame с транзакциями.
    """
    logging.info(f"✅ Файл {filepath} загружается...")

    df = pd.read_excel(filepath)

    # Приводим названия колонок к единому формату
    df.columns = df.columns.str.strip()

    # Приводим дату операции к формату datetime
    if "Дата операции" in df.columns:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

    # Заполняем пропущенные значения
    df.fillna("", inplace=True)

    logging.info(f"✅ Загружено {len(df)} записей.")

    return df
