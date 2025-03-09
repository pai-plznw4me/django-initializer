import pandas as pd
from datetime import datetime


def project_sync():
    filepath = './project/static/project/계약서리스트.xlsx'
    df = pd.read_excel(filepath)
    for ind, row in df.iterrows():
        code, name, alias, start, end, size, customer = row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[8]


if __name__ == '__main__':
    project_sync()
