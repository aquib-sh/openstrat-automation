""" =============================== OpenStrat Kernel ====================================
    Author: Shaikh Aquib
     
    Serves as a backbone in connecting various service that would be used by OpenStrat class.
    This is the only layer which OpenStrat bot will interact to get the service from other classes.
"""
import io
from bot import BotMaker
from symbols import SymbolScraper
from csv_parser import CSVParser

class OpenStratKernel:

    def __init__(self):
        self.BROWSER = "Firefox"
        self.HEADLESS_MODE = False
        self.CALENDAR_CALL = "https://optionstrat.com/build/diagonal-call-spread/"
        self.VERBOSE = True

        self.symbols = None
        self.bot = None
        self.scraper = SymbolScraper()
        self.parser = CSVParser() 

    def load_symbols(self) -> None:
        message1 = "Loading Stock Symbols..."
        message2 = "[OK] Loaded Stock Symbols"
        if self.VERBOSE:print(message1)
        #=====================================================
        symbol_data = self.scraper.fetch_symbols()
        self.symbols = self.parser.text_to_dataframe(symbol_data) 
        #=====================================================
        if self.VERBOSE:print(message2)

    def start_browser_engine(self) -> None:
        message1 = f"Starting {self.BROWSER} Browser Engine..."
        message2 = f"[OK] Started {self.BROWSER} Browser Engine"
        if self.VERBOSE:print(message1)
        #=====================================================
        self.bot = BotMaker(browser=self.BROWSER, behead=self.HEADLESS_MODE)
        #=====================================================
        if self.VERBOSE:print(message2)

    def shutdown_browser_engine(self) -> None:
        message1 = f"Stopping {self.BROWSER} Browser Engine..."
        message2 = f"[OK] Stopped {self.BROWSER} Browser Engine"
        if self.VERBOSE:print(message1)
        #=====================================================
        self.bot.shutdown()
        #=====================================================
        if self.VERBOSE:print(message2)
        
    def load_calendar_call(self, symbol:str):
        message1 = f"Loading Calendar Call Page for {symbol}..."
        message2 = f"[OK] Loaded Calendar Call Page for {symbol}"
        if self.VERBOSE:print(message1)
        #=====================================================
        self.bot.move(self.CALENDAR_CALL+symbol)
        #=====================================================
        if self.VERBOSE:print(message2)
    






