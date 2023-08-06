import time
import typing

import ExtremePluginManager.background.base_thread as base_thread


class DelayedTask(base_thread.BaseThread):
    def __init__(
            self, delay: float, target: typing.Union[callable, None], *args, **kwargs
    ) -> None:
        super().__init__(target, *args, **kwargs)
        self._delay = delay

    def _behavior(self):
        time.sleep(self._delay)
        self._execute()
