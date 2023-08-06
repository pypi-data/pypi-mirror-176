import abc
import json
import os.path
import sys
import traceback
import typing

import ExtremePluginManager.background.background_task as background_task
import ExtremePluginManager.background.delayed_task as delayed_task
import ExtremePluginManager.background.interval_task as interval_task
import ExtremePluginManager.constants as constants

if typing.TYPE_CHECKING:
    import ExtremePluginManager.extreme_plugin_manager as extreme_plugin_manager


class BasePlugin(abc.ABC):
    def __init__(
            self, parent, path: constants.PATH_TYPEHINT, builtin_funcs: dict, info_filename: str = "info.json",
            code_filename: str = "main.py"
    ):
        self._plugin_manager: 'extreme_plugin_manager.ExtremePluginManager' = parent
        self._path = path
        self._builtin_funcs = builtin_funcs.copy()
        self._info_filename = info_filename
        self._code_filename = code_filename

        self._info: dict = json.loads(self._get_info_data())
        self._plugin_id: str = self._info["id"]

        self._builtin_funcs.update({
            "read_file_bytes": self.read_file_bytes,
            "write_file_bytes": self.write_file_bytes,
            "remove_file": self.remove_file,
            "info": self.info,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "plugin_manager": self._plugin_manager,
            "plugin": self,
            "start_background_task": lambda target, *args, **kwargs: background_task.BackgroundTask(
                target, *args, **kwargs
            ),
            "start_delayed_task": lambda delay, target, *args, **kwargs: delayed_task.DelayedTask(
                delay, target, *args, **kwargs
            ),
            "start_interval_task": lambda interval, target, *args, **kwargs: interval_task.IntervalTask(
                interval, target, *args, **kwargs
            )
        })

        self._bytecode = {}

    def __repr__(self):
        return "<EPM Plugin id={} path={} type={}>".format(
            repr(self._plugin_id), repr(os.path.abspath(self._path)), repr(self.plugin_type)
        )

    def reload(self):
        self._bytecode = self._builtin_funcs.copy()

        path = os.path.abspath(self._path)
        sys.path.append(path)

        try:
            exec(self._get_main_code_file(), self._bytecode)
            self._plugin_manager.on_plugin_load(self)

        except Exception as e:
            self._bytecode = self._builtin_funcs.copy()

            self._plugin_manager.on_plugin_exception(
                self, traceback.format_exc().replace(
                    "<string>",
                    os.path.abspath(os.path.join(self._path, self._code_filename))
                ), e
            )

        try:
            sys.path.remove(path)

        except ValueError:
            pass

    def _get_info_data(self) -> str:
        return self.read_file(self._info_filename)

    @abc.abstractmethod
    def read_file_bytes(self, path: constants.PATH_TYPEHINT) -> bytes:
        pass

    @abc.abstractmethod
    def write_file_bytes(self, path: constants.PATH_TYPEHINT, contents: bytes):
        pass

    @abc.abstractmethod
    def remove_file(self, path: constants.PATH_TYPEHINT):
        pass

    @staticmethod
    @abc.abstractmethod
    def is_plugin_type(path: constants.PATH_TYPEHINT):
        pass

    def _get_main_code_file(self) -> str:
        return self.read_file(self._code_filename)

    @property
    def path(self) -> constants.PATH_TYPEHINT:
        return self._path

    def get_path(self) -> constants.PATH_TYPEHINT:
        return self._path

    @property
    def info(self) -> dict:
        return self._info

    def get_info(self) -> dict:
        return self._info

    @property
    def plugin_manager(self) -> 'extreme_plugin_manager.ExtremePluginManager':
        return self._plugin_manager

    def get_plugin_manager(self) -> 'extreme_plugin_manager.ExtremePluginManager':
        return self._plugin_manager

    @property
    def plugin_id(self) -> str:
        return self._plugin_id

    def get_plugin_id(self) -> str:
        return self._plugin_id

    @property
    def plugin_type(self) -> str:
        return self.__class__.__name__

    def get_plugin_type(self) -> str:
        return self.__class__.__name__

    def read_file(self, path: constants.PATH_TYPEHINT, encoding: str = "utf-8") -> str:
        return self.read_file_bytes(path).decode(encoding)

    def write_file(self, path: constants.PATH_TYPEHINT, contents: str, encoding: str = "utf-8"):
        return self.write_file_bytes(path, contents.encode(encoding))

    def execute_event(self, event: str, *args, **kwargs):
        path = os.path.abspath(self._path)
        sys.path.append(path)

        result = None

        try:
            if event in self._bytecode:
                result = self._bytecode[event](*args, **kwargs)

        except Exception as e:
            self._plugin_manager.on_plugin_exception(
                self, traceback.format_exc().replace(
                    "<string>",
                    os.path.abspath(os.path.join(self._path, self._code_filename))
                ), e
            )

        try:
            sys.path.remove(path)
        except ValueError:
            pass

        return result

    def kill(self):
        self._plugin_manager._plugins.remove(self)
        self.execute_event(self._plugin_manager._end_event)
