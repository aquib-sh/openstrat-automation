""" =============================== OpenStrat Kernel ====================================
    Author: Shaikh Aquib
     
    Serves as a backbone in connecting various service that would be used by OpenStrat class.
    This is the only layer which OpenStrat bot will interact to get the service from other classes.
"""
import io
import time
import re
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
        self.__FMONTH_START = 0
        self.__BMONTH_START = 17

        self.symbols = None
        self.bot = None
        self.scraper = SymbolScraper()
        self.parser = CSVParser() 
        self.fmonth_indx = self.__FMONTH_START
        self.bmonth_indx = self.__BMONTH_START

    def __click_body(self) -> None:
        self.bot.get_element_by_tag('body').click()

    def __prepare_soup(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self.bot.page_source(), 'lxml')

    def __get_net_debit(self, soup) -> str:
        for i in range(0, 5):
            elem = soup.find("span", string="Net Debit: ")
            if elem != None: 
                break
            else: 
                time.sleep(1)
                soup = self.__prepare_soup()

        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price

    def __get_max_loss(self, soup) -> str:
        for i in range(0, 5):
            elem = soup.find("span", string="Max loss: ")
            if elem != None: 
                break
            else:
                time.sleep(1)
                soup = self.__prepare_soup()

        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price
 
    def __get_max_profit(self, soup) -> str:
        for i in range(0, 5):
            elem = soup.find("span", string="Max profit: ")
            if elem != None:
                break
            else:
                time.sleep(1)
                soup = self.__prepare_soup()

        siblings = elem.parent.findChildren()
        price_elem = siblings[-1]
        price = price_elem.text
        return price
        
    def __get_breakevens(self, soup) -> str:
        for i in range(0, 10):
            elem = soup.find("span", string="Breakeven: ")
            if elem == None:
                elem = soup.find("span", string="Breakevens: ")
            if elem != None:
                break
            else:
                time.sleep(1)
                soup = self.__prepare_soup()

        siblings = elem.parent.findChildren()
        price_elem = siblings[-3]
        price = price_elem.text
        return price
 
    def __get_chance_of_profit(self, soup) -> str:
        for i in range(0, 5):
            elem = soup.find("span", string="Chance of Profit: ")
            if elem != None:
                break
            else:
                time.sleep(1)
                soup = self.__prepare_soup()

        gfather = elem.parent.parent
        price_elem = gfather.find_all('span')[3] 
        price = price_elem.text
        return price

    def __get_fmonth(self, soup) -> str:
        for i in range(1, 10):
            elem = soup.find('div', {"class":re.compile('^StrategyDetails_input__header__')})
            if elem != None:
                break
            else:
                time.sleep(1)
                soup = self.__prepare_soup()

        span = elem.find('span')
        date = span.text
        return date

    def __get_bmonth(self, soup) -> str:
        for i in range(0, 5):
            elem = soup.find_all('div', {"class":re.compile('^StrategyDetails_input__header__')})
            if elem != None:
                elem = elem[1]
                break
            else:
                time.sleep(1)     
                soup = self.__prepare_soup()

        span = elem.find('span')
        date = span.text
        return date

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
        info = {'FrontMonth':None,
                'BackMonth':None,
                'NetDebit':None,
                'MaxLoss':None,
                'MaxProfit':None,
                'BreakEvens':None,
                'ChanceOfProfit':None}

        soup = self.__prepare_soup()
        front_month = self.__get_fmonth(soup)
        back_month = self.__get_bmonth(soup)
        net_debit = self.__get_net_debit(soup)
        max_loss = self.__get_max_loss(soup)
        max_profit = self.__get_max_profit(soup)
        break_evens = self.__get_breakevens(soup)
        chance_of_profit = self.__get_chance_of_profit(soup)

        info['FrontMonth'] = front_month
        info['BackMonth'] = back_month
        info['NetDebit'] = net_debit
        info['MaxLoss'] = max_loss 
        info['MaxProfit'] = max_profit 
        info['BreakEvens'] = break_evens
        info['ChanceOfProfit'] = chance_of_profit 

        return info

    def goto_fmonth(self, indx) -> int:
        all_elems = self.bot.get_elements("//div[starts-with(@class, 'SeriesSelector_table__exp__')]")
        if ((indx < len(all_elems)) and (indx < self.__FMONTH_START)):
            all_elems[indx].click()
            return 1
        return -1

    def goto_bmonth(self, indx) -> int:
        all_elems = self.bot.get_elements("//div[starts-with(@class, 'SeriesSelector_table__exp__')]")
        if ((indx < len(all_elems)) and (indx > self.__FMONTH_START)):
            all_elems[indx].click()
            return 1
        return -1





    






