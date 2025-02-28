import pytest
import json
import datetime
import pandas as pd
from unittest.mock import patch
from src.views import generate_main_page


@pytest.fixture
def sample_transactions():
    """Создаёт тестовые транзакции для проверки"""
    data = [
        {"Дата операции": "2025-02-01T10:00:00", "Сумма операции": -1000.0, "Номер карты": "*1234"},
        {"Дата операции": "2025-02-05T15:30:00", "Сумма операции": -2500.0, "Номер карты": "*5678"},
        {"Дата операции": "2025-02-07T18:45:00", "Сумма операции": -750.0, "Номер карты": "*9876"},
    ]
    return pd.DataFrame(data)


@pytest.fixture
def mock_api_responses():
    """Создаёт фиктивные API-ответы для курсов валют и акций"""
    return {
        "currency_rates": [
            {"currency": "USD", "rate": 98.5},
            {"currency": "EUR", "rate": 105.2}
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 150.12},
            {"stock": "MSFT", "price": 296.71}
        ]
    }


@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_generate_main_page(mock_stocks, mock_currencies, sample_transactions, mock_api_responses):
    """Тестирует `generate_main_page`, проверяя корректность ответа"""
    mock_currencies.return_value = mock_api_responses["currency_rates"]
    mock_stocks.return_value = mock_api_responses["stock_prices"]

    current_time = "2025-02-10 10:30:00"
    response = generate_main_page(sample_transactions, current_time)

    assert isinstance(response, dict)
    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

    assert len(response["cards"]) == 3
    assert len(response["top_transactions"]) == 3
    assert len(response["currency_rates"]) == 2
    assert len(response["stock_prices"]) == 2

    # Проверка приветствия (утро/день/вечер)
    assert response["greeting"] == "Доброе утро"

    # Проверка корректности расчёта кешбэка
    assert response["cards"][0]["cashback"] == 10.0  # 1% от 1000
    assert response["cards"][1]["cashback"] == 25.0  # 1% от 2500
    assert response["cards"][2]["cashback"] == 7.5   # 1% от 750

    # Проверка курсов валют
    assert response["currency_rates"][0]["currency"] == "USD"
    assert response["currency_rates"][1]["currency"] == "EUR"

    # Проверка стоимости акций
    assert response["stock_prices"][0]["stock"] == "AAPL"
    assert response["stock_prices"][1]["stock"] == "MSFT"
