import time
import typing

import ExtremePluginManager.background.base_thread as base_thread


class IntervalTask(base_thread.BaseThread):
    def __init__(
            self, interval: float, target: typing.Union[callable, None], *args, **kwargs
    ) -> None:
        super().__init__(target, *args, **kwargs)
        self._interval = interval

    def get_interval(self) -> float:
        return self._interval

    def set_interval(self, interval: float):
        self._interval = interval

    def _behavior(self):
        while True:
            time.sleep(self._interval)
            self._execute()
