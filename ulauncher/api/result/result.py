from typing import Callable, Optional

from ulauncher.api.shared.action.BaseAction import BaseAction
from ulauncher.modes.Query import Query
from ulauncher.utils.text_highlighter import highlight_text
from ulauncher.utils.display import get_monitor_scale_factor

OnEnterCallback = Optional[Callable[[Query], Optional[BaseAction]]]


# pylint: disable=too-many-instance-attributes
class Result:

    ICON_SIZE = 40
    UI_FILE = 'result'

    score = None  # used by SortedResultList class to maintain sorted by score order of items

    _name = None  # type: str
    _description = None  # type: str
    _keyword = None  # type: str
    _icon = None  # type: Optional[str]
    _selected_by_default = False  # type: bool
    _on_enter = None  # type: OnEnterCallback
    _on_alt_enter = None  # type: OnEnterCallback
    _highlightable = True  # type: bool
    _is_extension = False  # type: bool

    # pylint: disable=too-many-arguments
    def __init__(self,
                 name: str = '',
                 description: str = '',
                 keyword: str = '',
                 icon: str = None,
                 selected_by_default: bool = False,
                 highlightable: bool = True,
                 on_enter: OnEnterCallback = None,
                 on_alt_enter: OnEnterCallback = None):
        if not isinstance(name, str):
            raise TypeError(f'"name" must be of type "str", "{type(name).__name__}" given')
        if not isinstance(description, str):
            raise TypeError(f'"description" must be of type "str", "{type(description).__name__}" given')
        if not isinstance(keyword, str):
            raise TypeError(f'"keyword" must be of type "str", "{type(keyword).__name__}" given')
        self._name = name
        self._description = description
        self._keyword = keyword
        self._icon = icon
        self._selected_by_default = selected_by_default
        self._on_enter = on_enter
        self._on_alt_enter = on_alt_enter
        self._highlightable = highlightable

    @classmethod
    def get_icon_size(cls):
        return cls.ICON_SIZE * get_monitor_scale_factor()

    def get_keyword(self) -> str:
        """
        If keyword is defined, search will be performed by keyword, otherwise by name.
        """
        return self._keyword

    def get_name(self) -> str:
        return self._name

    def get_name_highlighted(self, query: Query, color: str) -> Optional[str]:
        """
        :param ~ulauncher.modes.Query.Query query:
        :param str color:
        :rtype: str
        """
        if query and self._highlightable:
            return highlight_text(
                query if not self._is_extension else query.get_argument(''),
                self.get_name(),
                open_tag=f'<span foreground="{color}">',
                close_tag='</span>'
            )
        # don't highlight if query is empty
        return self.get_name()

    # pylint: disable=unused-argument
    def get_description(self, query: Query) -> str:
        """
        optional

        :param ~ulauncher.modes.Query.Query query:
        """
        return self._description

    def get_icon(self):
        """
        optional

        :rtype: str path to icon or themed icon name
        """
        return self._icon

    def selected_by_default(self, query):
        """
        Return True if item should be selected by default
        """
        return self._selected_by_default

    def on_enter(self, query: Query) -> Optional[BaseAction]:
        """
        :param ~ulauncher.modes.Query.Query query: it is passed only if :meth:`get_keyword` is implemented.
                                                    This allows you to create flows with a result item
        :rtype: :class:`~ulauncher.api.shared.action.BaseAction.BaseAction`
        """
        return self._on_enter(query) if callable(self._on_enter) else None

    def on_alt_enter(self, query: Query) -> Optional[BaseAction]:
        """
        Optional alternative enter

        :param ~ulauncher.modes.Query.Query query: it is passed only if :meth:`get_keyword` is implemented.
                                                    This allows you to create flows with a result item
        :rtype: :class:`~ulauncher.api.shared.action.BaseAction.BaseAction`
        """
        return self._on_alt_enter(query) if callable(self._on_alt_enter) else None
