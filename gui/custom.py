from Qt import QtWidgets, QtGui, QtCore


class QLineView(QtWidgets.QListView):
    """
    Subclass QListView to create a model controlled LineEdit like widget
    """

    def __init__(self, height=20):
        super(QLineView, self).__init__()

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.clicked.connect(lambda index: self.edit(index))
        self.setFixedHeight(height)

        model = QtGui.QStandardItemModel()
        self.item = QtGui.QStandardItem()

        # this offsets the text to be relatively center
        self.item.setSizeHint(QtCore.QSize(-1, height-5))

        # model.dataChanged.connect(self.func)
        model.setItem(0, 0, self.item)
        self.setModel(model)
