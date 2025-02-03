import os
from dotenv import load_dotenv
from external_api import get_exchange_rate  # Импортируем функцию получения курса валют

# Загружаем переменные окружения
load_dotenv()

# Проверяем, загружен ли API-ключ
API_KEY = os.getenv("EXCHANGE_API_KEY")
print(f"API_KEY загружен? {'ДА' if API_KEY else 'НЕТ'}")

# Если API-ключ загружен, получаем и выводим курсы валют
if API_KEY:
    try:
        usd_to_rub = get_exchange_rate("USD")
        eur_to_rub = get_exchange_rate("EUR")
        print(f"1 USD = {usd_to_rub:.2f} RUB")
        print(f"1 EUR = {eur_to_rub:.2f} RUB")
    except ValueError as e:
        print(f"Ошибка: {e}")
