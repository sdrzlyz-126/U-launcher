import mock
import pytest
from gi.repository import Gdk
from ulauncher.modes.file_browser.FileBrowserMode import FileBrowserMode
from ulauncher.modes.file_browser.FileQueries import FileQueries
from ulauncher.utils.Path import InvalidPathError


class TestFileBrowserMode:

    @pytest.fixture
    def path(self, mocker):
        return mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Path').return_value

    @pytest.fixture
    def file_queries(self):
        return mock.create_autospec(FileQueries)

    @pytest.fixture
    def SetUserQueryAction(self, mocker):
        return mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.SetUserQueryAction')

    @pytest.fixture
    def mode(self, file_queries, mocker):
        FileQueriesMock = mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.FileQueries')
        FileQueriesMock.get_instance.return_value = file_queries
        return FileBrowserMode()

    def test_is_enabled(self, mode):
        assert mode.is_enabled('~/Downloads')
        assert mode.is_enabled('~')
        assert mode.is_enabled('$USER/Videos')
        assert mode.is_enabled('/usr/bin')
        assert mode.is_enabled('/')
        assert mode.is_enabled(' /foo/bar')

        assert not mode.is_enabled('test')
        assert not mode.is_enabled('+')
        assert not mode.is_enabled(' ')

    def test_list_files(self, mode, mocker, file_queries):
        listdir = mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.os.listdir')
        listdir.return_value = ['a', 'd', 'b', 'c']
        file_queries.find.side_effect = lambda i: i
        assert mode.list_files('path') == sorted(listdir.return_value)
        assert mode.list_files('path', sort_by_usage=True) == sorted(listdir.return_value, reverse=True)

    def test_create_result(self, mode, mocker):
        FileBrowserResult = mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.FileBrowserResult')
        Path = mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Path')
        assert mode.create_result('path') == FileBrowserResult.return_value
        FileBrowserResult.assert_called_once_with(Path.return_value)
        Path.assert_called_once_with('path')

    def test_filter_dot_files(self, mode):
        assert mode.filter_dot_files(['a', '.b', 'c', '.d']) == ['a', 'c']

    def test_handle_query__path_from_q_exists__dir_listing_rendered(self, mode, path, mocker):
        path.get_existing_dir.return_value = '/tmp/dir'
        path.get_abs_path.return_value = path.get_existing_dir.return_value
        mocker.patch.object(mode, 'list_files', return_value=['a', 'd', 'b', 'c'])
        mocker.patch.object(mode, 'create_result', side_effect=lambda i: i)
        assert mode.handle_query('/tmp/dir') == ['/tmp/dir/a', '/tmp/dir/d', '/tmp/dir/b', '/tmp/dir/c']

    def test_handle_query__InvalidPathError__empty_list_rendered(self, mode, path):
        path.get_existing_dir.side_effect = InvalidPathError()
        assert mode.handle_query('~~') == []

    def test_handle_key_press_event(self, mode, mocker, SetUserQueryAction):
        mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Gdk.keyval_name', return_value='BackSpace')
        widget = mock.MagicMock()
        event = mock.MagicMock()
        event.state = 0
        query = '/usr/bin/'
        widget.get_position.return_value = len(query)
        widget.get_selection_bounds.return_value = tuple()
        mode.handle_key_press_event(widget, event, query)

        SetUserQueryAction.assert_called_with('/usr/')
        widget.emit_stop_by_name.assert_called_with('key-press-event')

    def test_handle_key_press_event__not_backspace(self, mode, mocker, SetUserQueryAction):
        mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Gdk.keyval_name', return_value='Enter')
        widget = mock.MagicMock()
        event = mock.MagicMock()
        event.state = 0
        query = '/usr/bin/'
        widget.get_position.return_value = len(query)
        mode.handle_key_press_event(widget, event, query)

        assert not SetUserQueryAction.called
        assert not widget.emit_stop_by_name.called

    def test_handle_key_press_event__ctrl_pressed(self, mode, mocker, SetUserQueryAction):
        mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Gdk.keyval_name', return_value='BackSpace')
        widget = mock.MagicMock()
        event = mock.MagicMock()
        event.state = Gdk.ModifierType.MOD2_MASK | Gdk.ModifierType.CONTROL_MASK
        query = '/usr/bin/'
        widget.get_position.return_value = len(query)
        mode.handle_key_press_event(widget, event, query)

        assert not SetUserQueryAction.called
        assert not widget.emit_stop_by_name.called

    def test_handle_key_press_event__wrong_cursor_position(self, mode, mocker, SetUserQueryAction):
        mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Gdk.keyval_name', return_value='BackSpace')
        widget = mock.MagicMock()
        event = mock.MagicMock()
        event.state = 0
        query = '/usr/bin/'
        widget.get_position.return_value = 3
        mode.handle_key_press_event(widget, event, query)

        assert not SetUserQueryAction.called
        assert not widget.emit_stop_by_name.called

    def test_handle_key_press_event__not_dir(self, mode, mocker, SetUserQueryAction):
        mocker.patch('ulauncher.modes.file_browser.FileBrowserMode.Gdk.keyval_name', return_value='BackSpace')
        widget = mock.MagicMock()
        event = mock.MagicMock()
        event.state = 0
        query = '/usr/b/'
        widget.get_position.return_value = len(query)
        mode.handle_key_press_event(widget, event, query)

        assert not SetUserQueryAction.called
        assert not widget.emit_stop_by_name.called
