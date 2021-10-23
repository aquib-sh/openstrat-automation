import requests

class SymbolScraper:

    def __init__(self):
        self.url = "https://www.cboe.com/us/options/symboldir/weeklys_options/?download=csv"

    def fetch_symbols(self):
        response = requests.get(self.url)
        contents = response.content.decode()
        return contents





