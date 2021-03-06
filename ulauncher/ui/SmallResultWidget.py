from ulauncher.ui.ResultWidget import ResultWidget


class SmallResultWidget(ResultWidget):
    """
    It is instantiated automagically if the following is done:
        - its name is set in .ui file in class attribute
        - __gtype_name__ is set to the same class name
        - this class is be imported somewhere in the code before .ui file is built
    """

    __gtype_name__ = "SmallResultWidget"
