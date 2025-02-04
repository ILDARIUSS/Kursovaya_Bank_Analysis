import datetime
import logging
from src.views import generate_main_page

# Настраиваем логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    logger.info("🚀 Запуск приложения...")
    json_output = generate_main_page(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(json_output)
