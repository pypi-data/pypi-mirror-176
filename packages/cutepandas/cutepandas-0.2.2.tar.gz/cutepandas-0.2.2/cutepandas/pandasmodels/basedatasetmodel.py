"""
@author: Philipp Temminghoff
"""

import logging
from typing import Optional

import pandas as pd
from prettyqt import constants, core, custom_models
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


class BaseDatasetModel(custom_models.BaseModelMixin, core.AbstractTableModel):

    dataset_updated = core.Signal(pd.DataFrame)
    MIME_TYPE = Optional[str]

    def __init__(self, ds: pd.DataFrame = None, parent: QtCore.QObject = None):
        """
        initalize our model
        """
        super().__init__(parent=parent)
        self.ds = ds
        self.do_sort = True

    def supportedDropActions(self):
        return constants.MOVE_ACTION

    def mimeTypes(self):
        return [self.MIME_TYPE]

    def mimeData(self, indexes) -> core.MimeData:
        """
        AbstractItemModel override, defines the data used for drag and drop
        atm this just returns the positions (not sure if this is perfect)
        """
        mime_data = core.MimeData()
        data = [i.row() for i in indexes if i.column() == 0]
        mime_data.set_json_data(self.MIME_TYPE, data)
        return mime_data

    def layoutchange_update(self, ds):
        with self.change_layout():
            self.ds = ds
        self.dataset_updated.emit(self.ds)

    def resetmodel_update(self, ds):
        with self.reset_model():
            self.ds = ds
        self.dataset_updated.emit(self.ds)

    def removerow_update(self, ds, start_index: int, stop_index: int):
        with self.remove_rows(start_index, stop_index):
            self.ds = ds
        self.dataset_updated.emit(self.ds)
