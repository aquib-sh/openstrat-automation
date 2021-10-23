import io
import pandas

class CSVParser:

    def __init__(self, text:str):
        self.text = text

    def to_dataframe(self) -> pandas.DataFrame:
        data = io.StringIO(self.text)
        return pandas.read_csv(data, sep=",")
