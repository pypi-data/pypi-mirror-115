import math
from functools import reduce
from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt


class Strategy(ABC):
    """ Стратегия """

    LONG = 'long'
    SHORT = 'short'

    def __init__(self, df: pd.DataFrame, params: dict):
        self.df = df
        self.set_params(params)

        self.trades = pd.DataFrame(columns=['open_time', 'close_time', 'open', 'close',
                                            'volume', 'profit', 'max_drawdown', 'max_possible_profit'])
        self.transactions = pd.DataFrame(columns=['open_time', 'close_time', 'open',
                                                  'close', 'profit'])

        self.current_opens = []
        self.position = 0
        self.av_price = 0
        self.drawdown = 0
        self.possible_profit = 0

        self.row = None
        self.index = 0

        self.lot_dollars = 10
        self.direction = self.LONG

        self.need_transactions = False

    def set_params(self, params: dict):
        """ Установить параметры стратегии """
        for param_name, value in params.items():
            self.__setattr__(param_name, value)

    def tune(self, lot_dollars: float = None, direction: str = None,
             need_transactions: bool = None):
        """ Установить параметры стратегии """
        for setting_name, value in locals().items():
            if value is not None:
                self.__setattr__(setting_name, value)

    def increase_position(self):
        """ Увеличить позицию """
        self.position += 1
        self.current_opens.append({
            'time': self.row['close_time'],
            'price': self.row['close']
        })
        self.av_price = reduce(lambda s, x: s + x['price'],  self.current_opens, 0) / len(self.current_opens)

    def close_position(self):
        """ Закрыть позицию """
        if self.need_transactions:
            self.calculate_transactions_profit()
        profit = self.calc_current_trade_profit()
        self.trades = self.trades.append({
                'open_time': self.current_opens[0]['time'],
                'close_time': self.row['close_time'],
                'open': self.current_opens[0]['price'],
                'close': self.row['close'],
                'volume': self.position,
                'profit': profit,
                'max_drawdown': self.drawdown,
                'max_possible_profit': self.possible_profit
        }, ignore_index=True)
        self.position = 0
        self.current_opens = []
        self.drawdown = math.inf
        self.possible_profit = -math.inf

    def calculate_transactions_profit(self):
        """ Рассчитать профит по отдельным сделкам """
        for open_data in self.current_opens:
            profit = self.calc_trade_profit(open_data['price'], self.row['close'], 1)
            self.transactions = self.transactions.append({
                'open_time' : open_data['time'],
                'close_time': self.row['close_time'],
                'open': open_data['price'],
                'close': self.row['close'],
                'profit': profit
            }, ignore_index=True)

    def calc_current_trade_profit(self) -> float:
        """ Рассчитать прибыль по текущей позиции """
        open_price = self.av_price
        close_price = self.row['close']
        return self.calc_trade_profit(open_price, close_price, self.position)

    def calc_trade_profit(self, open_price: float, close_price: float, volume: float) -> float:
        """ Сосчитать профит по сделке """
        diff = close_price - open_price
        if self.direction == self.SHORT:
            diff = -diff
        return self.lot_dollars * volume / open_price * (diff - 0.0004 * (close_price + open_price))

    def run(self):
        """ Запустить расчеты """
        self.trades = self.trades[self.trades['close_time'] == -1]
        self.transactions = self.transactions[self.transactions['close_time'] == -1]
        self.df['position'] = 0

        self.current_opens = []
        self.position = 0
        self.drawdown = math.inf
        self.possible_profit = -math.inf

        for index, row in self.df.iterrows():
            self.index = index
            self.row = row
            self.process_iterate()
            self.df.at[self.index, 'position'] = self.position
            if self.position != 0:
                current_profit = self.calc_current_trade_profit()
                self.drawdown = min(current_profit, self.drawdown)
                self.possible_profit = max(current_profit, self.drawdown)

    @abstractmethod
    def process_iterate(self):
        """ Обработать итерацию расчетов """
        pass

    def get_profit(self) -> float:
        """ Получить профит по стратегии """
        return self.trades['profit'].sum()

    def calc_coef(self) -> float:
        """ Рассчитать коэффициент """
        coef = 0
        for index, row in self.trades.iterrows():
            if row['profit'] < 0:
                coef += row['profit'] + 1.05 ** row['profit'] - 1
            else:
                coef += row['profit']
        return coef

    def draw_cum(self):
        """ Отрисовать кумуляту сделок """
        plt.plot(self.trades['close_time'].values, self.trades['profit'].cumsum().values)
        plt.show()

    def draw_cum_and_price(self):
        """ Отрисовать кумуляту сделок и цену"""
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(self.df['close_time'].values, self.df['close'].values, label='Цена', color='darkred')
        ax2.plot(self.trades['close_time'].values, self.trades['profit'].cumsum().values, label='Прибыль')
        ax1.set_ylabel('Цена')
        ax2.set_ylabel('Прибыль')
        fig.legend()
        plt.show()

    @staticmethod
    def draw_positions(df, need_av_enter=True):
        """ Отрисовать позиции на датафрейме """
        df = df.reset_index()
        df['pos_diff'] = df['position'].diff()
        trade_inputs = df[df['pos_diff'] > 0]
        trade_outputs = df[df['pos_diff'] < 0]
        plt.plot(df['close_time'].values, df['close'].values, color='orange')
        plt.plot(df['close_time'].values, df['ma'].values)
        if need_av_enter:
            av_price = trade_inputs['close'].mean()
            plt.plot(
                [df['close_time'][0], df['close_time'][len(df) - 1]],
                [av_price, av_price],
                linestyle='--',
                color='#9EF5A1'
            )
        plt.scatter(trade_inputs['close_time'].values, trade_inputs['close'].values, marker="^", c='green', zorder=10)
        plt.scatter(trade_outputs['close_time'].values, trade_outputs['close'].values, marker="v", c='red', zorder=10)
        plt.show()

    def get_df_by_trade_index(self, trade_index: int) -> pd.DataFrame:
        """ Получить датафрейм по индексу сделки """
        start_ts = self.trades['open_time'][trade_index]
        end_ts = self.trades['close_time'][trade_index]
        return self.df[(self.df['close_time'] >= start_ts) & (self.df['close_time'] <= end_ts)]
