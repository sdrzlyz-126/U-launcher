import pytest
import mock
from gi.repository import GdkPixbuf

from ulauncher.api import Result
from ulauncher.ui.ResultWidget import ResultWidget


# pylint: disable=too-many-public-methods
class TestResultWidget:

    @pytest.fixture
    def item_obj(self):
        return mock.create_autospec(Result)

    @pytest.fixture(autouse=True)
    def Theme(self, mocker):
        return mocker.patch('ulauncher.ui.ResultWidget.Theme')

    @pytest.fixture
    def result_wgt(self, builder, item_obj):
        result_wgt = ResultWidget()
        result_wgt.initialize(builder, item_obj, 3, 'query')
        return result_wgt

    @pytest.fixture
    def item_box(self, result_wgt):
        return result_wgt.item_box

    @pytest.fixture(autouse=True)
    def builder(self):
        return mock.MagicMock()

    @pytest.fixture
    def pixbuf(self):
        return mock.Mock(spec=GdkPixbuf.Pixbuf)

    def test_initialize(self, builder, item_obj, mocker):
        result_wgt = ResultWidget()
        set_index = mocker.patch.object(result_wgt, 'set_index')
        set_name = mocker.patch.object(result_wgt, 'set_name')
        set_description = mocker.patch.object(result_wgt, 'set_description')

        result_wgt.initialize(builder, item_obj, 3, 'query')

        builder.get_object.return_value.connect.assert_any_call("button-release-event", result_wgt.on_click)
        builder.get_object.return_value.connect.assert_any_call("enter_notify_event", result_wgt.on_mouse_hover)
        set_index.assert_called_with(3)
        set_name.assert_called_with(item_obj.get_name_highlighted.return_value)
        set_description.assert_called_with(item_obj.get_description.return_value)
        item_obj.get_description.assert_called_with('query')

    def test_set_index(self, result_wgt, mocker):
        mock_set_shortcut = mocker.patch.object(result_wgt, 'set_shortcut')

        result_wgt.set_index(2)
        mock_set_shortcut.assert_called_once_with('Alt+3')

    def test_select(self, result_wgt, item_box, mocker):
        mock_get_style_context = mocker.patch.object(item_box, 'get_style_context')
        result_wgt.select()
        mock_get_style_context.return_value.add_class.assert_called_once_with('selected')

    def test_deselect(self, result_wgt, item_box, mocker):
        mock_get_style_context = mocker.patch.object(item_box, 'get_style_context')
        result_wgt.deselect()
        mock_get_style_context.return_value.remove_class.assert_called_once_with('selected')

    def test_set_icon(self, result_wgt, builder, pixbuf):
        iconWgt = mock.MagicMock()
        builder.get_object.return_value = iconWgt

        result_wgt.set_icon(pixbuf)
        iconWgt.set_from_pixbuf.assert_called_with(pixbuf)

    def test_set_name(self, result_wgt, builder):
        result_wgt.set_name('test name')
        builder.get_object.return_value.set_text.assert_called_with('test name')

    def test_on_click(self, mocker, result_wgt):
        mock_get_toplevel = mocker.patch.object(result_wgt, 'get_toplevel')

        result_wgt.set_index(3)
        result_wgt.on_click(None, None)
        mock_get_toplevel.return_value.select_result.assert_called_with(3)
        mock_get_toplevel.return_value.enter_result.assert_called_with(alt=False)

    def test_on_click_alt_enter(self, mocker, result_wgt):
        mock_get_toplevel = mocker.patch.object(result_wgt, 'get_toplevel')

        event = mock.MagicMock()
        event.button = 3
        result_wgt.set_index(3)
        result_wgt.on_click(None, event)
        mock_get_toplevel.return_value.select_result.assert_called_with(3)
        mock_get_toplevel.return_value.enter_result.assert_called_with(alt=True)

    def test_on_mouse_hover(self, mocker, result_wgt):
        mock_get_toplevel = mocker.patch.object(result_wgt, 'get_toplevel')

        result_wgt.set_index(4)
        result_wgt.on_mouse_hover(None, None)
        mock_get_toplevel.return_value.select_result.assert_called_with(4, onHover=True)

    def test_set_description(self, result_wgt, builder):
        result_wgt.set_description('test description')
        builder.get_object.return_value.set_text.assert_called_with('test description')

    def test_no_description(self, result_wgt, builder):
        result_wgt.set_description(None)
        builder.get_object.return_value.destroy.assert_called_with()

    def test_set_shortcut(self, result_wgt, builder):
        result_wgt.set_shortcut('Alt+1')
        builder.get_object.return_value.set_text.assert_called_with('Alt+1')

    def test_on_enter(self, result_wgt, item_obj):
        assert result_wgt.on_enter('test') is item_obj.on_enter.return_value
        item_obj.on_enter.assert_called_with('test')

    def test_on_alt_enter(self, result_wgt, item_obj):
        assert result_wgt.on_alt_enter('test') is item_obj.on_alt_enter.return_value
        item_obj.on_alt_enter.assert_called_with('test')

    def test_keyword(self, result_wgt, item_obj):
        assert result_wgt.get_keyword() is item_obj.keyword

    def test_selected_by_default(self, result_wgt, item_obj):
        assert result_wgt.selected_by_default('q') is item_obj.selected_by_default.return_value
