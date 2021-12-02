import logging

from ulauncher.api.server.ExtensionMode import ExtensionMode
from ulauncher.modes.apps.AppMode import AppMode
from ulauncher.modes.shortcuts.ShortcutMode import ShortcutMode
from ulauncher.modes.file_browser.FileBrowserMode import FileBrowserMode
from ulauncher.modes.calc.CalcMode import CalcMode
from ulauncher.utils.decorator.singleton import singleton

logger = logging.getLogger(__name__)


class Search:

    @classmethod
    @singleton
    def get_instance(cls):
        file_browser_mode = FileBrowserMode()
        calc_mode = CalcMode()
        shortcut_search_mode = ShortcutMode()
        extension_search_mode = ExtensionMode()
        app_search_mode = AppMode([shortcut_search_mode, extension_search_mode])
        return cls([file_browser_mode,
                    calc_mode,
                    shortcut_search_mode,
                    extension_search_mode,
                    app_search_mode])

    def __init__(self, search_modes):
        self.search_modes = search_modes

    def on_query_change(self, query):
        """
        Iterate over all search modes and run first enabled.
        AppMode is always enabled
        """
        for mode in self.search_modes:
            mode.on_query_change(query)

        self._choose_search_mode(query).handle_query(query).run()

    def on_key_press_event(self, widget, event, query):
        self._choose_search_mode(query).handle_key_press_event(widget, event, query).run()

    def _choose_search_mode(self, query):
        for mode in self.search_modes:
            if mode.is_enabled(query):
                return mode

        raise Exception('This line should not be entered')
