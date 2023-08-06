from time import sleep
from typing import Callable, Dict, Tuple, Type
from multiprocess import Pool
import numpy as np
import pandas as pd
import nevergrad as ng
from .Strategy import Strategy
import matplotlib.pyplot as plt


def calc_efficiency(train_profit: float, test_profit: float) -> float:
    if train_profit <= 0:
        return np.nan
    return round((test_profit / train_profit) * 100, 2)


def get_calc_strategy_func(strategy: Type[Strategy]) -> Callable:
    """ Получить функцию для расчета минимумов по стратегии """
    s = strategy

    def calc_strategy_profit(df, **params) -> float:
        s_obj = s()
        s_obj.tune(for_opt=True)
        s_obj.run(df, params)
        return -s_obj.coef
    return calc_strategy_profit


def find_best_params(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list]
) -> Tuple[float, Dict[str, float]]:
    """ Найти лучшие значения по стратегии """
    params = {}
    for param_name in param_ranges:
        params[param_name] = ng.p.TransitionChoice(param_ranges[param_name])
    parametrization = ng.p.Instrumentation(
        df=ng.p.TransitionChoice([df]),
        **params
    )
    optimizer = ng.optimizers.NGOpt(parametrization=parametrization, budget=100)
    recommendation = optimizer.minimize(calc_strategy)
    best_params = recommendation.kwargs
    del best_params['df']
    best_coef = calc_strategy(df, **best_params)
    return -best_coef, best_params


class Epoch:
    """ Данные по эпохе """

    def __init__(self):
        self.task = None

        self.df_train: pd.DataFrame = None
        self.df_test: pd.DataFrame = None

        self.strategy_train: Strategy = None
        self.strategy_test: Strategy = None

        self.is_done = False

    def get_train_ts(self) -> Dict[str, int]:
        """ Получить временные метки эпохи обучения """
        return {
            'start': int(self.df_train['close_time'][0] / 1000),
            'end': int(self.df_train['close_time'][len(self.df_train) - 1] / 1000)
        }

    def get_test_ts(self) -> Dict[str, int]:
        """ Получить временные метки эпохи теста """
        return {
            'start': int(self.df_test['close_time'][0] / 1000),
            'end': int(self.df_test['close_time'][len(self.df_test) - 1] / 1000)
        }


class Forward:
    """ Форвардный анализ """

    def __init__(self):
        self.result: pd.DataFrame = None

        self.df: pd.DataFrame = None
        self.param_ranges = {}
        self.strategy: Type[Strategy] = None

        self.epoch_strategies = {}

        self.train_window = 0
        self.test_window = 0
        self.train_window_days = 0
        self.test_window_days = 0

        self.epochs_data: Dict[int, Epoch] = {}

        self.pool: Pool = None
        self.done_tasks = 0

    def run(self, strategy: Type[Strategy], df: pd.DataFrame, param_ranges: Dict[str, list],
            train_window_days: int, test_window_days: int):
        """ Запустить форвардный анализ """
        self.df = df
        self.param_ranges = param_ranges
        self.strategy = strategy

        self.result = pd.DataFrame(
            columns=['epoch', 'coef_eff', 'train_rel_profit', 'test_profit'] + list(param_ranges.keys())
        )

        self.train_window_days = train_window_days
        self.test_window_days = test_window_days

        self.train_window = train_window_days * 24 * 60
        self.test_window = test_window_days * 24 * 60

        self.init_epochs_data()
        self.done_tasks = 0

        self.pool = Pool(processes=12)
        try:
            self.create_tasks()
            self.monitor_tasks()
        finally:
            self.pool.close()

    def init_epochs_data(self):
        """ Инициализировать данные по эпохам """
        epochs = int((len(self.df) - self.train_window) / self.test_window)
        for epoch in range(epochs):
            self.epochs_data[epoch] = Epoch()

            epoch_start_learn = epoch * self.test_window
            epoch_end_learn = epoch_start_learn + self.train_window
            self.epochs_data[epoch].df_train = self.df[epoch_start_learn:epoch_end_learn].reset_index(drop=True)

            epoch_start_test = epoch_end_learn
            epoch_end_test = epoch_start_test + self.test_window
            self.epochs_data[epoch].df_test = self.df[epoch_start_test:epoch_end_test].reset_index(drop=True)

    def create_tasks(self):
        """ Создать задачи """
        for epoch, epoch_data in self.epochs_data.copy().items():
            self.epochs_data[epoch].task = self.pool.apply_async(find_best_params, (
                get_calc_strategy_func(self.strategy),
                epoch_data.df_train,
                self.param_ranges
            ))

    def monitor_tasks(self):
        """ Мониторить задачи """
        total_tasks = len(self.epochs_data)
        while self.done_tasks < total_tasks:
            print("\r ", end="")
            print(f' leave epochs: {self.done_tasks}/{total_tasks}'.ljust(40), end="")
            for epoch, epoch_data in self.epochs_data.items():
                if epoch_data.is_done is False and epoch_data.task.ready():
                    self.done_tasks += 1
                    self.epochs_data[epoch].is_done = True
                    train_coef, best_params = epoch_data.task.get()

                    test_strategy = self.strategy()
                    test_strategy.run(epoch_data.df_test, best_params)
                    test_profit = test_strategy.get_profit()

                    train_strategy = self.strategy()
                    train_strategy.run(epoch_data.df_train, best_params)
                    train_profit = train_strategy.get_profit()
                    train_rel_profit = train_profit * self.test_window_days / self.train_window_days

                    self.result = self.result.append({
                        'epoch': epoch,
                        'train_coef': train_coef,
                        'train_rel_profit': train_rel_profit,
                        'test_profit': test_profit,
                        'coef_eff': calc_efficiency(train_rel_profit, test_profit),
                        **best_params
                    }, ignore_index=True)
                    self.epochs_data[epoch].strategy_test = test_strategy
                    self.epochs_data[epoch].strategy_train = train_strategy
            sleep(0.1)

        print("\r ", end="")
        print(f' leave epochs: {self.done_tasks}/{total_tasks}'.ljust(40))
        self.result = self.result.sort_values('epoch').reset_index(drop=True)

    def get_epoch(self, number: int) -> Epoch:
        """ Получить эпоху """
        return self.epochs_data[number]

    def draw_train_profit(self):
        plt.plot(self.result['train_rel_profit'].cumsum())
        plt.show()

    def draw_test_profit(self):
        plt.plot(self.result['test_profit'].cumsum())
        plt.show()

    def draw_profit(self):
        plt.plot(self.result['test_profit'].cumsum())
        plt.plot(self.result['train_rel_profit'].cumsum())
        plt.show()


