import pandas as pd
import logging

logger = logging.getLogger(__name__)

def read_excel_transactions(filepath: str) -> pd.DataFrame:
    """
    Загружает данные о транзакциях из Excel-файла.
    """
    try:
        df = pd.read_excel(filepath)
        logger.info(f"✅ Файл {filepath} успешно загружен. Найдено {len(df)} записей.")
        return df
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке {filepath}: {e}")
        return pd.DataFrame()
