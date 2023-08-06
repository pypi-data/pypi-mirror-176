from __future__ import annotations

from pyqtgraph.parametertree import Parameter, parameterTypes as ptypes
from pyqtgraph.parametertree.Parameter import PARAM_TYPES
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from qtextras import fns
from qtextras.widgets.lineeditor import PopupLineEditor

__all__ = [
    "KeySequenceParameterItem",
    "ParameterDialog",
    "PgParameterDelegate",
    "PgPopupDelegate",
    "PopupLineEditorParameterItem",
    "PopupLineEditorParameter",
]


class MonkeyPatchedTextParameterItem(ptypes.TextParameterItem):
    def makeWidget(self):
        textBox: QtWidgets.QTextEdit = super().makeWidget()
        textBox.setTabChangesFocus(True)
        return textBox


# Monkey patch pyqtgraph text box to allow tab changing focus
ptypes.TextParameter.itemClass = MonkeyPatchedTextParameterItem


class ParameterDialog(QtWidgets.QDialog):
    def __init__(self, param: Parameter, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.param = param
        self.tree = fns.flexibleParameterTree(param)
        self.saveChanges = False

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tree)

        okBtn = QtWidgets.QPushButton("Ok")
        cancelBtn = QtWidgets.QPushButton("Cancel")
        btnLay = QtWidgets.QHBoxLayout()
        btnLay.addWidget(okBtn)
        btnLay.addWidget(cancelBtn)
        layout.addLayout(btnLay)

        def okClicked():
            self.saveChanges = True
            self.accept()

        def cancelClicked():
            self.saveChanges = False
            self.reject()

        okBtn.clicked.connect(okClicked)
        cancelBtn.clicked.connect(cancelClicked)


class PgPopupDelegate(QtWidgets.QStyledItemDelegate):
    """
    For pyqtgraph-registered parameter types that don't define an itemClass with
    `makeWidget`, this popup delegate can be used instead which creates a popout
    parameter tree.
    """

    def __init__(self, paramDict: dict, parent=None):
        super().__init__(parent)
        paramDict.setdefault("name", paramDict["type"])
        self.param = Parameter.create(**paramDict)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        self.param.setValue(index.data(QtCore.Qt.ItemDataRole.EditRole))
        editor = ParameterDialog(self.param)
        editor.show()
        editor.resize(editor.width() + 50, editor.height() + 30)

        return editor

    def setModelData(
        self,
        editor: QtWidgets.QWidget,
        model: QtCore.QAbstractTableModel,
        index: QtCore.QModelIndex,
    ):
        if editor.saveChanges:
            model.setData(index, editor.param.value())

    def setEditorData(self, editor: QtWidgets.QWidget, index):
        value = index.data(QtCore.Qt.ItemDataRole.EditRole)
        self.param.setValue(value)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        return


class PgParameterDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parameterDict: dict, parent=None):
        super().__init__(parent)
        errMsg = (
            f"`{self.__class__}` can only create parameter editors from registered"
            f" pyqtgraph widgets whose items subclass `WidgetParameterItem` and are in"
            f" pyqtgraph's `PARAM_TYPES`.\n"
            f"These requirements are not met for type `{parameterDict['type']}`"
        )

        if parameterDict["type"] not in PARAM_TYPES:
            raise TypeError(errMsg)
        parameterDict.update(name="dummy")
        self.param = param = Parameter.create(**parameterDict)
        item = param.makeTreeItem(0)
        if isinstance(item, ptypes.WidgetParameterItem):
            self.item = item
        else:
            raise TypeError(errMsg)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        # TODO: Deal with params that go out of scope before yielding a value
        editor = self.item.makeWidget()
        editor.setParent(parent)
        editor.setMaximumSize(option.rect.width(), option.rect.height())
        return editor

    def setModelData(
        self,
        editor: QtWidgets.QWidget,
        model: QtCore.QAbstractTableModel,
        index: QtCore.QModelIndex,
    ):
        model.setData(index, editor.value())

    def setEditorData(self, editor: QtWidgets.QWidget, index):
        value = index.data(QtCore.Qt.ItemDataRole.EditRole)
        editor.setValue(value)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        editor.setGeometry(option.rect)


class KeySequenceParameterItem(ptypes.WidgetParameterItem):
    """
    Class for creating custom shortcuts. Must be made here since pyqtgraph doesn't
    provide an implementation.
    """

    def makeWidget(self):
        item = QtWidgets.QKeySequenceEdit()

        item.sigChanged = item.editingFinished
        item.value = lambda: item.keySequence().toString()

        def setter(val: QtGui.QKeySequence):
            if val is None or len(val) == 0:
                item.clear()
            else:
                item.setKeySequence(val)

        item.setValue = setter
        self.param.seqEdit = item

        return item

    def updateDisplayLabel(self, value=None):
        # Make sure the key sequence is human-readable
        self.displayLabel.setText(self.widget.keySequence().toString())


class PopupLineEditorParameterItem(ptypes.WidgetParameterItem):
    def __init__(self, param, depth):
        strings = param.opts.get("limits", [])
        self.model = QtCore.QStringListModel(strings)
        param.sigLimitsChanged.connect(
            lambda _param, limits: self.model.setStringList(limits)
        )
        super().__init__(param, depth)

    def makeWidget(self):
        opts = self.param.opts
        editor = PopupLineEditor(
            model=self.model,
            clearOnComplete=False,
            forceMatch=opts.get("forceMatch", True),
            validateCase=opts.get("validateCase", False),
        )
        editor.setValue = editor.setText
        editor.value = editor.text
        editor.sigChanged = editor.editingFinished
        return editor

    def widgetEventFilter(self, obj, ev):
        # Prevent tab from leaving widget
        return False


class PopupLineEditorParameter(Parameter):
    itemClass = PopupLineEditorParameterItem

    def __init__(self, **opts):
        if "value" in opts:
            limits = opts.get("limits", [])
            if opts["value"] not in limits:
                limits.insert(0, opts["value"])
            opts["limits"] = limits
        super().__init__(**opts)


class DisplayValueParameterItem(ptypes.StrParameterItem):
    def makeWidget(self):
        widget = super().makeWidget()
        widget.setValue = lambda val: widget.setText(str(val))
        widget.value = self.param.value
        return widget

    def __init__(self, param, depth):
        super().__init__(param, depth)
        self.widget.setReadOnly(True)
        if param.value() is None:
            # Force set initial value if "None" otherwise it won't get set
            # Because pg.eq() will say value never needed to be initially set
            self.widget.setText("None")
            self.updateDisplayLabel()


class DisplayValueParameter(ptypes.SimpleParameter):
    itemClass = DisplayValueParameterItem

    def __init__(self, **opts):
        opts.update(enabled=False)
        super().__init__(**opts)

    def _interpretValue(self, v):
        return v


ptypes.registerParameterType("display", DisplayValueParameter, override=True)
ptypes.registerParameterItemType("keysequence", KeySequenceParameterItem, override=True)
ptypes.registerParameterType("popuplineeditor", PopupLineEditorParameter, override=True)
