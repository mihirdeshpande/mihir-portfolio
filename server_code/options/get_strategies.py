import concurrent.futures
import copy
import time
from datetime import datetime

import pandas as pd
import yfinance as yf

from server_code.options.call_credit_spread import CallCreditStrategy
from server_code.options.consts import BASIC_INFO_COLUMNS
from server_code.options.most_traded_symbols import MOST_TRADED_SYMBOLS
from server_code.options.put_credit_spread import PutCreditStrategy
from server_code.options.utils import add_daily_moves


class OptionStrategies:

    def __init__(self, budget):
        self.budget = budget
        self.__symbols_info_df = None
        self.all_strategies = list()

    @staticmethod
    def get_basic_info_row(symbol_ticker):
        return [symbol_ticker.info.get(key, None) for key in BASIC_INFO_COLUMNS]

    @staticmethod
    def are_weekly_options_available(symbol_ticker):
        options = symbol_ticker.options
        if not options or len(options) < 2:
            return False
        options_1_date = datetime.strptime(options[0], '%Y-%m-%d')
        options_2_date = datetime.strptime(options[1], '%Y-%m-%d')
        if (options_2_date - options_1_date).days > 7:
            return False
        return True

    def __populate_symbols_info(self):
        tickers_object = yf.Tickers(MOST_TRADED_SYMBOLS)
        self.tickers_info = tickers_object.tickers  # tickers_info: {symbol: yfinance.Ticker}
        rows = []
        for symbol, symbol_ticker in self.tickers_info.items():
            try:
                if self.are_weekly_options_available(symbol_ticker):
                    new_row = self.get_basic_info_row(symbol_ticker)
                    rows.append(new_row)
            except Exception as ex:
                pass
        self.__symbols_info_df = pd.DataFrame(rows, columns=BASIC_INFO_COLUMNS)
        x = 1

    def __get_ticker_data(self, symbol, symbol_ticker):
        try:
            if self.are_weekly_options_available(symbol_ticker):
                return self.get_basic_info_row(symbol_ticker)
        except Exception as ex:
            return None

    def __populate_symbols_info_threaded(self):
        tickers_object = yf.Tickers(MOST_TRADED_SYMBOLS)
        self.tickers_info = tickers_object.tickers  # tickers_info: {symbol: yfinance.Ticker}
        rows = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self.__get_ticker_data, symbol, symbol_ticker)
                for symbol, symbol_ticker in self.tickers_info.items()
            ]

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

            # Retrieve the results from the futures (ticker data or None for failed requests)
            rows = [future.result() for future in futures if future.result()]

        self.__symbols_info_df = pd.DataFrame(rows, columns=BASIC_INFO_COLUMNS)

    @property
    def symbols_info(self):
        if self.__symbols_info_df is None:
            self.__populate_symbols_info_threaded()
        return self.__symbols_info_df

    def get_put_credit_spreads(self):
        put_strategy = PutCreditStrategy(copy.deepcopy(self.__symbols_info_df),
                                         self.budget, self.tickers_info)
        put_strategies = put_strategy.get_put_credit_strategies()
        # self.all_strategies.extend(put_strategies)
        return put_strategies

    def get_call_credit_spreads(self):
        call_strategy = CallCreditStrategy(copy.deepcopy(self.__symbols_info_df),
                                           self.budget, self.tickers_info)
        call_strategies = call_strategy.get_call_credit_strategies()
        # self.all_strategies.extend(call_strategies)
        return call_strategies

    def clean_info_df(self):
        self.__symbols_info_df = self.__symbols_info_df.dropna(
            subset=['currentPrice'])

    def process_info_df(self):
        self.clean_info_df()
        add_daily_moves(self.__symbols_info_df)

    def setup(self):
        # self.__populate_symbols_info()
        self.__populate_symbols_info_threaded()
        self.process_info_df()


def get_strategies(budget):
    print("Starting 10 thread...")
    option_strategies = OptionStrategies(budget=budget)
    start_time = time.time()
    option_strategies.setup()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Setup Done in: {elapsed_time:.6f} seconds")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit the functions to the executor
        put_credit_spreads = executor.submit(option_strategies.get_put_credit_spreads)
        call_credit_spreads = executor.submit(option_strategies.get_call_credit_spreads)

        # Wait for both futures to complete
        concurrent.futures.wait([put_credit_spreads, call_credit_spreads])

    print("Strategies Generated!")
    option_strategies.all_strategies.extend(put_credit_spreads.result() + call_credit_spreads.result())
    option_strategies.all_strategies.sort(key=lambda x: x['profit_to_risk'], reverse=True)
    return option_strategies.all_strategies


if __name__ == '__main__':
    strategies = get_strategies(budget=1000)
    x = 1
