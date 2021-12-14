from ulauncher.api import Result
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.modes.QueryHistoryDb import QueryHistoryDb


class ExtensionKeywordResult(Result):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._query_history = QueryHistoryDb.get_instance()

    def selected_by_default(self, query):
        """
        :param ~ulauncher.modes.Query.Query query:
        """
        return self._query_history.find(query) == self.get_name()

    def on_enter(self, query):
        """
        :param ~ulauncher.modes.Query.Query query: query
        """
        self._query_history.save_query(query, self.get_name())
        return SetUserQueryAction('%s ' % self.get_keyword())
