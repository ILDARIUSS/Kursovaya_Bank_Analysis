import datetime
import logging
from typing import List, Dict

import pandas as pd
import re

logger = logging.getLogger(__name__)


def process_transactions(transactions: List[Dict]) -> List[Dict]:
    pattern = re.compile(r"\w+\s\w\.")

    result = []
    for transaction in transactions:
        if transaction['Категория'] != 'Переводы':
            continue

        if pattern.match(transaction['Описание']):
            result.append(transaction)

    return result




if __name__ == '__main__':
    df = pd.read_excel('../data/operations.xlsx')
    data = df.to_dict(orient='records')
    result = process_transactions(data)
    print(result)