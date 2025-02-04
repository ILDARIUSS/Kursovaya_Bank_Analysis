import os
import requests
import logging
from dotenv import load_dotenv

# Настраиваем логгер
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загружаем переменные окружения
load_dotenv()
API_KEY = os.getenv("EXCHANGE_API_KEY")

if not API_KEY:
    logger.error("❌ API-ключ не найден! Проверь файл .env")
    raise ValueError("API-ключ отсутствует. Укажите EXCHANGE_API_KEY в .env файле.")

def get_exchange_rate(currency: str) -> float:
    """
    Получает курс валюты относительно рубля с API Apilayer.

    :param currency: Код валюты (например, 'USD', 'EUR')
    :return: Курс валюты по отношению к рублю
    """
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}  # Меняем base, чтобы API выдавал USD→RUB, EUR→RUB

    logger.info("🔍 Отправляем запрос в API: %s", url)
    logger.info("📌 Заголовки: %s", headers)
    logger.info("📌 Параметры запроса: %s", params)

    response = requests.get(url, headers=headers, params=params)

    try:
        data = response.json()
        logger.info("📩 Ответ API: %s", data)

        if not data.get("success") or "rates" not in data:
            raise ValueError(f"Ошибка API: {response.status_code} - {data}")

        return float(data["rates"]["RUB"])  # Получаем курс RUB

    except requests.exceptions.RequestException as e:
        logger.error("❌ Ошибка при запросе к API: %s", e)
        raise
