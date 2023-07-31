from server_code.options.utils import find_friday_in_future, split_contract


class PutCreditStrategy:
    def __init__(self, symbols_info_df, budget, tickers_info, max_strategies=5):
        self.symbols_info_df = symbols_info_df
        self.budget = budget
        self.tickers_info = tickers_info
        self.max_strategies = max_strategies
        self.put_credit_list = list()
        self.expiry_date = find_friday_in_future(35)
        self.expiry_date_str = self.expiry_date.strftime('%Y-%m-%d')

    def check_options_history(self, row):
        ticker_option_dates = self.tickers_info[row['symbol']].options
        if self.expiry_date_str not in ticker_option_dates:
            return
        puts = self.tickers_info[row['symbol']].option_chain(date=self.expiry_date_str).puts
        # 1. Find strike 1 just below currentPrice --> sell put
        put_sell_idx = -2
        for i in range(len(puts)):
            contract = puts.iloc[i]['contractSymbol']
            contract_dict = split_contract(contract)
            if contract_dict['strike'] > row['currentPrice']:
                break
            put_sell_idx += 1
        # 2. Find strike 2 below strike 1 --> buy put
        put_buy_idx = put_sell_idx - 1

        if put_buy_idx < 0:
            return
        # 3. Calculate ratio: max. profit / max. loss = (price1 - price2) / (strike1 - strike2)
        sell_price = (puts.iloc[put_sell_idx]['bid'] + puts.iloc[put_sell_idx]['ask']) / 2
        sell_spread = puts.iloc[put_sell_idx]['ask'] - puts.iloc[put_sell_idx]['bid']
        buy_price = (puts.iloc[put_buy_idx]['bid'] + puts.iloc[put_buy_idx]['ask']) / 2
        buy_spread = puts.iloc[put_buy_idx]['ask'] - puts.iloc[put_buy_idx]['bid']

        sell_strike = puts.iloc[put_sell_idx]['strike']
        buy_strike = puts.iloc[put_buy_idx]['strike']

        if sell_price <= buy_price:
            return
        if sell_strike - buy_strike > 5:
          return

        max_profit = round((sell_price - buy_price) * 100)
        max_loss = round((sell_strike - buy_strike) * 100) - max_profit
        profit_to_risk = round(max_profit / max_loss if max_loss != 0 else -1, 2)
        min_investment = max_loss

        # Checks for filtering out bad selections
        if min_investment > self.budget:
            return
        if ((sell_spread + buy_spread) / (sell_strike - buy_strike)) > 0.05:
            return
        if profit_to_risk < 0.25:
            return

        self.put_credit_list.append({'name': 'Put Credit Spread', 'symbol': row['symbol'], 'price': row['currentPrice'],
                                     'max_profit': max_profit, 'max_loss': max_loss,
                                     'suggested_strike': '{sell_strike}/{buy_strike} and below'.format(
                                         sell_strike=sell_strike, buy_strike=buy_strike),
                                     'min_investment': min_investment, 'suggested_expiry': self.expiry_date_str,
                                     'profit_to_risk': profit_to_risk, 'company': row['shortName']
                                     })

    def clean_data(self):
        # Get only stocks with negative move today
        self.symbols_info_df = self.symbols_info_df[self.symbols_info_df['dailyMove'] < 0]

    def get_put_credit_strategies(self):
        self.clean_data()
        for index, row in self.symbols_info_df.iterrows():
            try:
                self.check_options_history(row)
            except Exception as ex:
                pass
        self.put_credit_list.sort(key=lambda x: x['profit_to_risk'], reverse=True)
        return self.put_credit_list if len(self.put_credit_list) < self.max_strategies else self.put_credit_list[:self.max_strategies]
