import pandas as pd
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

class Retained :
    def __init__(self) :
        filename = str(ROOT) + "/retained/files/dataset.xlsx"
        self.df = pd.read_excel(filename)

    def retainedData(self) :
        df = self.df.head(10)
        df_list = df.to_dict('list')

        return df_list