import datetime
import json
import logging
from src.views import generate_main_page
from src.utils import read_excel_transactions

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Запуск приложения...")

    # Генерация главной страницы
    logger.info("🚀 Генерация главной страницы...")
    main_page_json = generate_main_page(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Вывод JSON на экран
    print(json.dumps(main_page_json, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
