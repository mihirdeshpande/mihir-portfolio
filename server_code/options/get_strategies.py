import copy

import pandas as pd
import yfinance as yf

from datetime import datetime
from server_code.options.most_traded_symbols import MOST_TRADED_SYMBOLS
from server_code.options.consts import BASIC_INFO_COLUMNS
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
        self.tickers_info = tickers_object.tickers   # tickers_info: {symbol: yfinance.Ticker}
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

    @property
    def symbols_info(self):
        if self.__symbols_info_df is None:
            self.__populate_symbols_info()
        return self.__symbols_info_df

    def get_put_credit_spreads(self):
        put_strategy = PutCreditStrategy(copy.deepcopy(self.__symbols_info_df), self.budget, self.tickers_info)
        put_strategies = put_strategy.get_put_credit_strategies()
        self.all_strategies.extend(put_strategies)

    def clean_info_df(self):
        self.__symbols_info_df = self.__symbols_info_df.dropna(subset=['currentPrice'])

    def process_info_df(self):
        self.clean_info_df()
        add_daily_moves(self.__symbols_info_df)

    def setup(self):
        self.__populate_symbols_info()
        self.process_info_df()
        x = 1


def get_strategies(budget):
    print("Starting...")
    option_strategies = OptionStrategies(budget=budget)
    option_strategies.setup()
    print("Setup Done...")
    option_strategies.get_put_credit_spreads()
    print("Below generated: ")
    # print(option_strategies.all_strategies)
    return option_strategies.all_strategies


if __name__ == '__main__':
    strategies = get_strategies(budget=1000)
    x = 1
