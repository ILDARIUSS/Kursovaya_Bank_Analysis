import pytest
import pandas as pd
from src.reports import generate_reports

@pytest.fixture
def sample_data():
    """Создаёт тестовый набор данных."""
    data = {
        "Дата операции": pd.date_range(start="2024-11-01", periods=10, freq="D"),
        "Сумма операции": [-100, 200, -50, 300, -400, 500, -600, 700, -800, 900]
    }
    return pd.DataFrame(data)

def test_generate_reports(sample_data):
    report = generate_reports(sample_data, "2025-02-05")
    assert "spending_by_weekday" in report
    assert isinstance(report["spending_by_weekday"], dict)
