""" =============================== OpenStrat Kernel ====================================
    Author: Shaikh Aquib
     
    Serves as a backbone in connecting various service that would be used by OpenStrat class.
    This is the only layer which OpenStrat bot will interact to get the service from other classes.
"""
import io
import bs4
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

    def __click_body(self) -> None:
        self.bot.get_element_by_tag('body').click()

    def __prepare_soup(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self.bot.page_source(), 'lxml')

    def __get_net_debit(self, soup) -> str:
        elem = soup.find("span", string="Net Debit: ")
        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price

    def __get_max_loss(self, soup) -> str:
        elem = soup.find("span", string="Max loss: ")
        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price
 
    def __get_max_profit(self, soup) -> str:
        elem = soup.find("span", string="Max profit: ")
        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price
        
    def __get_breakevens(self, soup) -> str:
        elem = soup.find("span", string="Breakeven: ")
        siblings = elem.parent.findChildren()
        price_elem = siblings[-3]
        price = price_elem.text
        return price
 
    def __get_chance_of_profit(self, soup) -> str:
        elem = soup.find("span", string="Chance of Profit: ")
        gfather = elem.parent.parent
        price_elem = gfather.find_all('span')[3] 
        price = price_elem.text
        return price

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
        """Loads the URL in browser engine for symbol calendar call."""
        message1 = f"Loading Calendar Call Page for {symbol}..."
        message2 = f"[OK] Loaded Calendar Call Page for {symbol}"
        if self.VERBOSE:print(message1)
        #=====================================================
        self.bot.move(self.CALENDAR_CALL+symbol)
        try:self.__click_body()
        except:pass
        #=====================================================
        if self.VERBOSE:print(message2)

    def fetch_calendar_call_info(self) -> dict:
        """Gets the info present on the page of calendar call page. 

        Returns:
            info:dict
            Dictionary containing the information of calendar call for that stock.
            Format:
                keys = {'NetDebit', 'MaxLoss', 'MaxFormat', 'BreakEvens', 'ChanceOfProfit'}
        """
        info = {'NetDebit':None,
                'MaxLoss':None,
                'MaxProfit':None,
                'BreakEvens':None,
                'ChanceOfProfit':None}

        soup = self.__prepare_soup()
        net_debit = self.__get_net_debit(soup)
        max_loss = self.__get_max_loss(soup)
        max_profit = self.__get_max_profit(soup)
        break_evens = self.__get_breakevens(soup)
        chance_of_profit = self.__get_chance_of_profit(soup)

        info['NetDebit'] = net_debit
        info['MaxLoss'] = max_loss 
        info['MaxProfit'] = max_profit 
        info['BreakEvens'] = break_evens
        info['ChanceOfProfit'] = chance_of_profit 

        return info


    






