from gi.repository import Gio
from ulauncher.utils.Settings import Settings
from ulauncher.modes.BaseMode import BaseMode
from ulauncher.modes.apps.AppResult import AppResult

settings = Settings.get_instance()


class AppMode(BaseMode):
    def get_searchable_items(self):
        disable_desktop_filters = settings.get_property('disable-desktop-filters')

        for app in Gio.DesktopAppInfo.get_all():
            executable = app.get_executable()
            show_in = app.get_show_in() or disable_desktop_filters
            # Make an exception for gnome-control-center, because all the very useful specific settings
            # like "Keyboard", "Wi-Fi", "Sound" etc have NoDisplay=true
            nodisplay = app.get_nodisplay() and not executable == 'gnome-control-center'
            if app.get_display_name() and executable and show_in and not nodisplay:
                yield AppResult(app)
