from vnpy.app.cta_strategy import (BarGenerator, ArrayManager)
from vnpy.trader.object import BarData, TickData
from vnpy.trader.constant import Interval
from typing import Callable
import talib


class NewBarGenerator(BarGenerator):
    ''''''

    def __init__(
            self,
            on_bar: Callable,
            window: int = 0,
            on_window_bar: Callable = None,
            interval: Interval = Interval.MINUTE
    ):
        super(NewBarGenerator, self).__init__(on_bar, window, on_window_bar, interval)

    def update_bar(self, bar: BarData):
        """
                Update 1 minute bar into generator
                """
        # If not inited, creaate window bar object
        if not self.window_bar:
            # Generate timestamp for bar data
            if self.interval == Interval.MINUTE:
                dt = bar.datetime.replace(second=0, microsecond=0)
            else:
                dt = bar.datetime.replace(minute=0, second=0, microsecond=0)

            self.window_bar = BarData(
                symbol=bar.symbol,
                exchange=bar.exchange,
                datetime=dt,
                gateway_name=bar.gateway_name,
                open_price=bar.open_price,
                high_price=bar.high_price,
                low_price=bar.low_price
            )
        # Otherwise, update high/low price into window bar
        else:
            self.window_bar.high_price = max(
                self.window_bar.high_price, bar.high_price)
            self.window_bar.low_price = min(
                self.window_bar.low_price, bar.low_price)

        # Update close price/volume into window bar
        self.window_bar.close_price = bar.close_price
        self.window_bar.volume += int(bar.volume)
        self.window_bar.open_interest = bar.open_interest

        # Check if window bar completed
        finished = False

        if self.interval == Interval.MINUTE:
            # # x-minute bar
            # if not (bar.datetime.minute + 1) % self.window:
            #     finished = True
            if self.last_bar and bar.datetime.minute != self.last_bar.datetime.minute:
                self.interval_count += 1
                if not self.interval_count % self.window:
                    finished = True
                    self.interval_count = 0

        elif self.interval == Interval.HOUR:
            if self.last_bar and bar.datetime.hour != self.last_bar.datetime.hour:
                # 1-hour bar
                if self.window == 1:
                    finished = True
                # x-hour bar
                else:
                    self.interval_count += 1

                    if not self.interval_count % self.window:
                        finished = True
                        self.interval_count = 0

        if finished:
            self.on_window_bar(self.window_bar)
            self.window_bar = None

        # Cache last bar object
        self.last_bar = bar


class NewArrayManager(ArrayManager):
    def __init__(self, size=100):
        super(NewArrayManager, self).__init__(size)

    def aroon(self, n, array=False):
        """
        AROON.
        """
        aroon_up, aroon_down = talib.AROON(
            self.high, self.low, n
        )
        if array:
            return aroon_up, aroon_down
        return aroon_up[-1], aroon_down[-1]







