import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def analyze_cashback(transactions: pd.DataFrame):
    """Анализ кешбэка по картам."""
    summary = transactions.groupby("Номер карты")["Сумма операции", "Кэшбэк"].sum().reset_index()
    summary.rename(columns={"Сумма операции": "total_spent", "Кэшбэк": "cashback"}, inplace=True)

    logging.info(f"📊 Анализ кешбэка:\n{summary.head(10)}")
    return summary.to_dict(orient="records")
