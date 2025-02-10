import json
import logging
import datetime
from src.utils import load_transactions
from src.views import generate_main_page
from src.services import process_transactions
from src.reports import generate_reports

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("🚀 Запуск главного модуля...")

    # Загружаем транзакции из файла
    transactions = load_transactions("data/operations.xlsx")

    # Генерация главной страницы
    logging.info("📊 Генерация главной страницы...")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    main_page_json = generate_main_page(transactions, current_time)

    print(json.dumps(main_page_json, indent=4, ensure_ascii=False))

    # Обработка транзакций (Сервис)
    logging.info("📊 Анализ транзакций за 01-2025")
    service_result = process_transactions(transactions, month=1, year=2025)

    # Конвертируем Timestamps в строки перед JSON-сериализацией
    for txn in service_result["transactions"]:
        txn["Дата операции"] = txn["Дата операции"].strftime("%Y-%m-%dT%H:%M:%S")

    print(json.dumps(service_result, indent=4, ensure_ascii=False))

    # Генерация отчета
    report_date = datetime.datetime.now().strftime("%Y-%m-%d")
    logging.info("📊 Генерация отчёта на %s", report_date)
    report_result = generate_reports(transactions, report_date)

    # Конвертируем Timestamps в строки перед JSON-сериализацией
    for date in report_result["spending_by_weekday"]:
        report_result["spending_by_weekday"][date] = float(report_result["spending_by_weekday"][date])

    print(json.dumps(report_result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
