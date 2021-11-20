import traceback
import time
from kernel import OpenStratKernel
from util import DataHandler

class OpenStrat:
    def __init__(self):
        self.info_keys=['Symbol',
                        'FrontMonth',
                        'BackMonth',
                        'NetDebit',
                        'MaxLoss',
                        'MaxProfit',
                        'BreakEvens',
                        'ChanceOfProfit'] 
        self.current_symbol = ""
        self.handler = DataHandler(self.info_keys)
        self.kernel = OpenStratKernel()
        self.kernel.HEADLESS_MODE=True
        self.kernel.start_browser_engine()

    def __fetch_and_put_info(self):
        i = y = fstatus = bstatus = 0
        self.kernel.reset_fmonth_indx() 

        while (fstatus != -1):
            fstatus = self.kernel.goto_fmonth(self.kernel.fmonth_indx)
            self.kernel.fmonth_indx += 1

            self.kernel.reset_bmonth_indx()
            bstatus = 0
    
            while (bstatus != -1):
                bstatus = self.kernel.goto_bmonth(self.kernel.bmonth_indx)
                self.kernel.bmonth_indx += 1

                try: 
                    info = self.kernel.fetch_calendar_call_info()
                except Exception as e:
                    continue
               
                info['Symbol'] = self.current_symbol
                self.handler.put(info)
                print(".", end="", flush=True)

    def get_data_by_symbol_iteration(self):
        i = 1
        INTERVAL = 10
        self.kernel.load_symbols()
        
        for symbol in self.kernel.read_symbols():
            self.current_symbol = symbol
            
            if (i % INTERVAL == 0):
                print("[*] Sleeping for 5 mins to avoid loading server")
                time.sleep(60*5)

            self.kernel.load_calendar_call(symbol)
            print("[+] Fetching info from page")
            try:
                self.__fetch_and_put_info()
            except:
                continue
            print("\n")
            print("====="*10)
            i += 1

    def save_data(self, fname="data.csv"):
        data = self.handler.as_dataframe()
        data.to_csv(fname, index=False)
        print(f"[+] Saved data to {fname}")

    def close(self):
        self.kernel.shutdown_browser_engine()

if __name__ == "__main__":
    app = OpenStrat()
    app.get_data_by_symbol_iteration()
    app.save_data()
    app.close()
