from typing import List, Dict, Union
import numpy as np
import pandas as pd


class DataProcessing:
    def __init__(self, data: List[Dict[str, Union[str, int]]]):
        self.df = None
        self.data = data

    def show_data(self) -> pd.DataFrame:
        return self.df.head()

    def create_dataframe(self) -> None:
        self.df = pd.DataFrame(
            self.data,
            columns=["Название тарифа", "Количество каналов", "Скорость доступа", "Абонентская плата"]
        )
        self.df = self.df.replace({np.nan: "null"})

    def save_data_as_excel(self, filename) -> None:
        self.df.to_excel(filename, index=False)