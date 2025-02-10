import logging
import pandas as pd
import datetime

logger = logging.getLogger(__name__)


def generate_reports(transactions, report_date):
    if isinstance(report_date, str):
        report_date = datetime.datetime.strptime(report_date, "%Y-%m-%d")

    logger.info(f"📊 Генерация отчёта с датой: {report_date.strftime('%Y-%m-%d')}")

    # Выборка за последние 3 месяца
    start_date = report_date - pd.DateOffset(months=3)
    logger.info(f"📅 Выборка данных с {start_date.strftime('%Y-%m-%d')} по {report_date.strftime('%Y-%m-%d')}")

    filtered_data = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= report_date)
        ]

    if filtered_data.empty:
        logger.warning("⚠️ Нет данных за выбранный период!")
        return {"spending_by_weekday": {}}

    spending_by_weekday = filtered_data.groupby(filtered_data["Дата операции"].dt.strftime("%A"))[
        "Сумма операции"].sum().to_dict()

    logger.info(f"📊 Траты по дням недели: {spending_by_weekday}")

    return {"spending_by_weekday": spending_by_weekday}
