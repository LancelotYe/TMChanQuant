from vnpy.app.cta_strategy import (CtaTemplate,BarGenerator,ArrayManager)
from vnpy.trader.object import BarData, TickData
from vnpy.trader.constant import Interval
from typing import Any
import python学习资料.VNProject.my_strategy_tool as mst


class DemoStrategy(CtaTemplate):
    author = "Tom"

    # 定义参数
    fast_window = 10
    slow_window = 2

    # 定义变量
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0

    rsi_count = 0

    parameters = [
        "fast_window",
        "slow_window"
    ]
    variables = [
        "fast_ma0",
        "fast_ma1",
        "slow_ma0",
        "slow_ma1"
        
        "rsi_count"
    ]

    def __init__(
            self,
            cta_engine: Any,
            strategy_name: str,
            vt_symbol: str,
            setting: dict,
    ):
        super(DemoStrategy, self).__init__(cta_engine, strategy_name, vt_symbol, setting)
        '''默认一分钟K线'''
        self.bg = BarGenerator(self.on_bar)
        '''自定义5分钟K线'''
        self.bg_5 = BarGenerator(self.on_bar, window=5, on_window_bar=self.on_5min_bar, interval=Interval.MINUTE)
        '''自定义7分钟K线'''
        self.bg_7 = mst.NewBarGenerator(self.on_bar, window=7, on_window_bar=self.on_7min_bar, interval=Interval.MINUTE)
        self.am = ArrayManager()

    def on_init(self):
        """策略初始化"""
        self.write_log("策略初始化")

        self.load_bar(10)

    def on_start(self):
        """启动"""
        self.write_log("策略启动")

    def on_stop(self):
        """停止"""
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """Tick更新"""
        # 速度快
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """K线更新"""
        self.bg_5.update_bar(bar)
        self.bg_7.update_bar(bar)

    def on_5min_bar(self, bar: BarData):

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        fast_ma = am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        '''判断均线交叉'''
        cross_over = (self.fast_ma0 >= self.slow_ma0 and
                      self.fast_ma1 < self.slow_ma1)

        cross_blow = (self.fast_ma0 <= self.slow_ma0 and
                      self.fast_ma1 > self.slow_ma1)

        if cross_over:
            price = bar.close_price + 5

            if not self.pos:
                self.buy(price, 1)
            elif self.pos < 0:
                self.cover(price, 1)
                self.buy(price, 1)
        elif cross_blow:
            price = bar.close_price - 5
            if not self.pos:
                self.short(price, 1)
            elif self.pos > 0:
                self.sell(price, 1)
                self.short(price, 1)

        # 更新图形界面
        self.put_event()

    def on_7min_bar(self, bar: BarData):
        # 指标条件逻辑
        am = self.am
        fast_rsi = am.rsi(self.fast_window, array=True)
        slow_rsi = am.rsi(self.slow_window, array=True)

        fast_rsi_0 = fast_rsi[-1]
        slow_rsi_0 = slow_rsi[-1]


        if fast_rsi_0 >= 70:
            print('over bought')
        elif fast_rsi_0 <= 30:
            print('over sold')

        # 上穿
        fast_rsi_1 = fast_rsi[-2]
        slow_rsi_1 = slow_rsi[-2]

        rsi_cross_over = (fast_rsi_1<slow_rsi_1, fast_rsi_0 >= slow_rsi_0)

        rsi_cross_blow = (fast_rsi_1>slow_rsi_1, fast_rsi_0 <= slow_rsi_0)

        if rsi_cross_blow:
            print('we buy')
        elif rsi_cross_over:
            print('we sell')


        if fast_rsi_0 > slow_rsi_0:
            self.rsi_count += 1
        else:
            self. rsi_count = 0

        if self.rsi_count >= 3:
            print('very strong up trend, we buy')

        pass

# class NewBarGenerator(BarGenerator):
#     ''''''
#
#     def __init__(
#             self,
#             on_bar: Callable,
#             window: int = 0,
#             on_window_bar: Callable = None,
#             interval: Interval = Interval.MINUTE
#     ):
#         super(NewBarGenerator, self).__init__(on_bar, window, on_window_bar, interval)
#
#
#     def update_bar(self, bar: BarData):
#         """
#                 Update 1 minute bar into generator
#                 """
#         # If not inited, creaate window bar object
#         if not self.window_bar:
#             # Generate timestamp for bar data
#             if self.interval == Interval.MINUTE:
#                 dt = bar.datetime.replace(second=0, microsecond=0)
#             else:
#                 dt = bar.datetime.replace(minute=0, second=0, microsecond=0)
#
#             self.window_bar = BarData(
#                 symbol=bar.symbol,
#                 exchange=bar.exchange,
#                 datetime=dt,
#                 gateway_name=bar.gateway_name,
#                 open_price=bar.open_price,
#                 high_price=bar.high_price,
#                 low_price=bar.low_price
#             )
#         # Otherwise, update high/low price into window bar
#         else:
#             self.window_bar.high_price = max(
#                 self.window_bar.high_price, bar.high_price)
#             self.window_bar.low_price = min(
#                 self.window_bar.low_price, bar.low_price)
#
#         # Update close price/volume into window bar
#         self.window_bar.close_price = bar.close_price
#         self.window_bar.volume += int(bar.volume)
#         self.window_bar.open_interest = bar.open_interest
#
#         # Check if window bar completed
#         finished = False
#
#         if self.interval == Interval.MINUTE:
#             # # x-minute bar
#             # if not (bar.datetime.minute + 1) % self.window:
#             #     finished = True
#             if self.last_bar and bar.datetime.minute != self.last_bar.datetime.minute:
#                 self.interval_count += 1
#                 if not self.interval_count % self.window:
#                     finished = True
#                     self.interval_count = 0
#
#         elif self.interval == Interval.HOUR:
#             if self.last_bar and bar.datetime.hour != self.last_bar.datetime.hour:
#                 # 1-hour bar
#                 if self.window == 1:
#                     finished = True
#                 # x-hour bar
#                 else:
#                     self.interval_count += 1
#
#                     if not self.interval_count % self.window:
#                         finished = True
#                         self.interval_count = 0
#
#         if finished:
#             self.on_window_bar(self.window_bar)
#             self.window_bar = None
#
#         # Cache last bar object
#         self.last_bar = bar