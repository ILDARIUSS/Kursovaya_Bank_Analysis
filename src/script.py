import json
import datetime
import logging
from src.views import generate_main_page
from src.utils import read_excel_transactions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Запуск приложения...")

    # Загружаем  операции
    transactions = read_excel_transactions("data/operations.xlsx")
    if transactions.empty:
        logger.warning("⚠️ Нет данных для анализа транзакций!")
        return

    # Получаем JSON для главной страницы
    main_page_json = generate_main_page(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Выводим результат
    print(json.dumps(main_page_json, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
