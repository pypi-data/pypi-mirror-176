import ExtremePluginManager.background.base_thread as base_thread


class BackgroundTask(base_thread.BaseThread):
    def _behavior(self):
        self._execute()
