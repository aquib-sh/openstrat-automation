import pandas

class DataHandler:
    """Data Hander Interface for easy data processing
    Adds, Appends, transforms data.

    Stores data as a dictionary of key:list values.
    """
    def __init__(self, keys:list):
        self.__data = {}
        for k in keys:
            self.__data[k] = []

    def key_present(self, _key) -> bool:
        return (_key in self.__data)

    def put(self, to_add:dict):
        """Appends dictionary data into internal data."""
        for (_key, value) in to_add.items():
            if (self.key_present(_key)): 
                self.__data[_key].append(value)

    def as_dataframe(self) -> pandas.DataFrame:  
        return (pandas.DataFrame(self.__data))



