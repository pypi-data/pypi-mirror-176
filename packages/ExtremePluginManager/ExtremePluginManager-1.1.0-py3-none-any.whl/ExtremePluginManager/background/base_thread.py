import ctypes
import threading
import typing
import abc


class ThreadKilledException(Exception):
    pass


class BaseThread(threading.Thread, abc.ABC):
    def __init__(self, target: typing.Union[callable, None], *args, **kwargs) -> None:
        self._target = target
        self._args = args
        self._kwargs = kwargs

        super().__init__(target=self._behavior, daemon=True)
        self.start()

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> 'BaseThread':
        self.name = name
        return self

    def _get_my_tid(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id

        for tid, thread_obj in threading._active.items():
            if thread_obj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def kill(self):
        if not self.is_alive():
            return

        tid = self._get_my_tid()

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(ThreadKilledException))
        if res == 0:
            raise ValueError("invalid thread id")

        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def _execute(self):
        self._target(*self._args, **self._kwargs)

    @abc.abstractmethod
    def _behavior(self):
        pass
