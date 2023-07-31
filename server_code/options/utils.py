from datetime import datetime, timedelta


def add_daily_moves(symbols_info_df):
    def daily_move(row):
        return (row['currentPrice'] - row['previousClose']) / row['previousClose']

    symbols_info_df['dailyMove'] = symbols_info_df.apply(daily_move, axis=1)


def find_friday_in_future(days_range):
    today = datetime.today().date()
    future_date = today + timedelta(days=days_range)
    # Find the next Friday
    while future_date.weekday() != 4:  # 4 corresponds to Friday (Monday is 0, Sunday is 6)
        future_date += timedelta(days=1)
    return future_date


def split_contract(contract):
    return {
        'strike': float(contract[-8:]) / 1000,
        'type': contract[-9],
        'expiry': contract[-15:-9],
        'symbol': contract[:-15]
    }
