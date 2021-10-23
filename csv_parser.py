import io
import pandas

class CSVParser:
    def text_to_dataframe(self, text:str) -> pandas.DataFrame:
        data = io.StringIO(text)
        return pandas.read_csv(data, sep=",")
