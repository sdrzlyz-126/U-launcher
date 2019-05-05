from distutils.version import StrictVersion
from gi.repository import Gtk


def gtk_version_is_gte(major: int, minor: int, micro: int) -> bool:
    gtk_version = '%s.%s.%s' % (Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())
    return StrictVersion(gtk_version) >= StrictVersion('%s.%s.%s' % (major, minor, micro))
