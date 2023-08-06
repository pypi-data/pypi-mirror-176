"""
@author: Philipp Temminghoff
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from prettyqt import constants, gui
from cutepandas import pandasmodels
from cutepandas.util import icons

logger = logging.getLogger(__name__)


def _(label: str) -> str:
    return label


class PandasIndexModel(pandasmodels.BaseDatasetModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, ds: pd.DataFrame, parent=None, read_only: bool = False):
        super().__init__(parent=parent, ds=ds)
        self.ds = ds
        self.is_read_only = read_only
        self.COLUMN_ROLE = constants.USER_ROLE + 20
        self.show_tooltips = False
        self.show_icons = False
        self.DEFAULT_FORMAT = "%.5g"

    def rowCount(self, parent=None):
        """
        override for AbstractitemModels
        """
        return min(len(self.ds.index), self.MAX_ROWS)

    def columnCount(self, parent=None):
        """
        override for AbstractitemModels
        """
        return len(self.ds.index.names)

    def data(self, index, role=constants.DISPLAY_ROLE):
        """
        override for AbstractitemModels
        EditRole: value as str
        DisplayRole: number-formatted value as str (+ "Preview" for last line")
        DTYPE_ROLE: dtype of feature
        NAME_ROLE: raw value
        COLUMN_ROLE: Name of feature
        """
        if not index.isValid():
            return None
        if role == constants.EDIT_ROLE:
            return str(self.cell_content(index.row(), index.column()))
        elif role == constants.BACKGROUND_ROLE:
            return gui.Color("lightgray")
            # row = index.row()
            # col = index.column()
            # if row == 0:
            #     return gui.Color("lightgray")
            # prev = self.index(row - 1, col)
            # return gui.Color("lightgray") if index.data() != prev.data() else None
        elif role == constants.DISPLAY_ROLE:
            row = index.row()
            if row == self.MAX_ROWS - 1:
                row = len(self.ds.index) - 1
            elif row == self.MAX_ROWS - 2:
                return "..."
            data = self.cell_content(row, index.column())
            if isinstance(data, (float, np.float32)):
                return self.DEFAULT_FORMAT % data
            return str(data)
        elif role == constants.TOOLTIP_ROLE and self.show_tooltips:
            idx = self.get_index(index.column())
            dtype = idx.dtype
            colname = idx.name
            return f"<b>{colname if colname else _('Index')}</b><br>Dtype: {dtype}"
        elif role == self.DTYPE_ROLE:
            return self.get_index(index.column()).dtype
        elif role == self.NAME_ROLE:
            return self.cell_content(index.row(), index.column())
        elif role == self.COLUMN_ROLE:
            return self.get_index(index.column()).name
        return None

    def flags(self, index):
        """
        override for AbstractitemModels
        """
        return super().flags(index) | constants.NO_CHILDREN

    def headerData(self, idx: int, orientation, role):
        """
        override for AbstractitemModels
        """
        if orientation == constants.HORIZONTAL:
            if role == constants.DISPLAY_ROLE:
                header = self.ds.index.names[idx]
                return str(header) if header is not None else _("Index")
            elif role == constants.DECORATION_ROLE and self.show_icons:
                return icons.icon_for_index(self.get_index(idx))
        return None

    def sort(self, ncol: int, order):
        """
        override for AbstractitemModels
        Sort table by given index col.
        """
        if not self.do_sort:
            return None
        logger.debug("sort() called for PandasIndexModel")
        with self.change_layout():
            is_ascending = order == constants.ASCENDING
            self.ds = self.ds.sort_values(
                by=self.ds.index.names[ncol], ascending=is_ascending
            )
        self.dataset_updated.emit(self.ds)

    def get_index(self, row: int | None = None):
        # using get_level_values() is too slow for large datasets with multiindex
        idx = self.ds.index
        return idx.levels[row] if isinstance(idx, pd.MultiIndex) else idx

    def cell_content(self, row: int, col: int | None):
        if isinstance(self.ds.index, pd.MultiIndex):
            return self.ds.iloc[row].name[col]
        else:
            return self.ds.index[row]


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    model = PandasIndexModel(df)
    widget = widgets.TableView()
    widget.set_model(model)
    widget.show()
    app.main_loop()
