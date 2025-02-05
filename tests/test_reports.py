import pandas as pd
from src.reports import generate_reports


def test_generate_reports():
    data = {
        "Дата операции": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "Сумма операции": [-1000, 500]
    }
    df = pd.DataFrame(data)
    result = generate_reports(df)

    assert "spending_by_weekday" in result
    assert isinstance(result["spending_by_weekday"], dict)
