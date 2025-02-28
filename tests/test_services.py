import pytest
from src.services import process_transactions

@pytest.fixture
def sample_data():
    """Создает тестовый набор данных."""
    return [
        {"Дата операции": "2025-01-31T14:55:15", "Сумма операции": -2500},
        {"Дата операции": "2025-02-10T14:55:15", "Сумма операции": -5000},
        {"Дата операции": "2025-02-05T10:00:00", "Сумма операции": -1500},
        {"Дата операции": "2024-12-20T09:30:00", "Сумма операции": -3500},
    ]

def test_process_transactions_january(sample_data):
    """Проверяет фильтрацию транзакций за январь 2025."""
    result = process_transactions(sample_data, 1, 2025)
    assert len(result) == 1
    assert result[0]["Сумма операции"] == -2500

def test_process_transactions_february(sample_data):
    """Проверяет фильтрацию транзакций за февраль 2025."""
    result = process_transactions(sample_data, 2, 2025)
    assert len(result) == 2  # Ожидаем 2 транзакции
    assert result[0]["Сумма операции"] == -5000
    assert result[1]["Сумма операции"] == -1500

def test_process_transactions_no_data(sample_data):
    """Проверяет, что пустой список возвращается, если нет транзакций за период."""
    result = process_transactions(sample_data, 3, 2025)  # В марте транзакций нет
    assert len(result) == 0
