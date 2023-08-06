"""
@author: Philipp Temminghoff
"""

import logging

import numpy as np
import pandas as pd

from prettyqt import constants, gui, widgets
from cutepandas import pandasmodels
from cutepandas.util import helpers, icons

logger = logging.getLogger(__name__)


class PandasModel(pandasmodels.BaseDatasetModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, ds=None, parent=None, read_only=False, color_values=False):
        super().__init__(parent=parent, ds=ds)
        self.is_read_only = read_only
        self.COLUMN_ROLE = constants.USER_ROLE + 20
        self.show_tooltips = False
        self.show_icons = False
        self.DEFAULT_FORMAT = "%.5g"
        self.max = None
        if color_values and (self.ds.shape[0] * self.ds.shape[1]) < 10000:
            try:
                self.max = self.ds.max().max()
            except TypeError:
                pass

    def rowCount(self, parent=None):
        """
        override for AbstractitemModels
        """
        return min(len(self.ds.index), self.MAX_ROWS)

    def columnCount(self, parent=None):
        """
        override for AbstractitemModels
        """
        return len(self.ds.columns)

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
            return str(self.ds.iat[index.row(), index.column()])
        elif role == constants.DISPLAY_ROLE:
            row = index.row()
            if row == self.MAX_ROWS - 1:
                row = len(self.ds.index) - 1
            elif row == self.MAX_ROWS - 2:
                return "..."
            data = self.ds.iat[row, index.column()]
            if isinstance(data, (float, np.float32)):
                return self.DEFAULT_FORMAT % data
            return str(data)
        elif role == constants.BACKGROUND_ROLE:
            col = index.column()
            dtype = self.ds.iloc[:, col].dtype
            data = self.ds.iat[index.row(), col]
            if pd.api.types.is_numeric_dtype(dtype) and self.max is not None:
                value = abs(data / self.max)
                return gui.Color.from_cmyk(0, value, value, 0).as_qt()
            elif isinstance(data, (bool, np.bool_)):
                color = gui.Color("green" if data else "red")
                color.setAlphaF(0.2)
                return color.as_qt()
        elif role == constants.TOOLTIP_ROLE and self.show_tooltips:
            dtype = str(self.ds.iloc[:, index.column()].dtype)
            colname = self.ds.iloc[:, index.column()].name
            return f"<b>{colname}</b><br>Dtype: {dtype}"
        elif role == self.DTYPE_ROLE:
            return self.ds.iloc[:, index.column()].dtype
        elif role == self.NAME_ROLE:
            return self.ds.iloc[index.row(), index.column()]
        elif role == self.COLUMN_ROLE:
            return self.ds.iloc[:, index.column()].name
        return None

    def setData(self, index, value, role=constants.EDIT_ROLE):
        """
        override for AbstractitemModels
        """
        if not index.isValid():
            return False
        if role == constants.EDIT_ROLE:
            row = index.row()
            col = index.column()
            dtype = self.ds[self.ds.columns[col]].dtype
            if helpers.infer_type(value) == self.ds.iloc[row, col]:
                return False
            try:
                # s = self.ds.iloc[:, index.column()]
                # if s.dtype == "category" and value not in s.cat.categories:
                #     s.cat.add_categories(value, inplace=True)
                if helpers.is_nan(value):
                    arg = "numpy.nan"
                elif pd.api.types.is_numeric_dtype(dtype):
                    arg = float(value)
                else:
                    arg = repr(value)
                self.ds.iat[row, col] = value
                self.ds.log(
                    f"|ds|.iat[{row}, {col}] = {arg}",
                    description=f"Change value {row}:{col} to {value}",
                    imports=["numpy"] if helpers.is_nan(value) else [],
                )
                self.dataset_updated.emit(self.ds)
                return True
            except ValueError as e:
                logger.exception(e)
                return False

    # def removeColumns(self, col, count, parent=None):
    #     """
    #     override for AbstractitemModels
    #     """
    #     # atm only working properly for count=1 (nothing else needed yet)
    #     end_col = col + count - 1
    #     cols = self.ds.columns.tolist()[col:end_col + 1]
    #     with self.remove_columns(col, col, parent):
    #         method = datasetmethods.DropMethod(labels=cols,
    #                                            axis=1,
    #                                            errors="ignore")
    #         self.ds = method.apply_method(self.ds)
    #     self.dataset_updated.emit(self.ds)
    #     return True

    def flags(self, index):
        """
        override for AbstractitemModels
        """
        cur_flags = super().flags(index) | constants.NO_CHILDREN
        return cur_flags if self.is_read_only else cur_flags | constants.IS_EDITABLE

    def headerData(self, idx: int, orientation, role):
        """
        override for AbstractitemModels
        """
        if orientation == constants.HORIZONTAL:
            if role == constants.ALIGNMENT_ROLE:
                return constants.ALIGN_CENTER | constants.ALIGN_BOTTOM
            elif role == constants.DISPLAY_ROLE:
                return helpers.format_name(self.ds.columns[idx])  # type: ignore
            elif role == constants.DECORATION_ROLE and self.show_icons:
                return icons.icon_for_dtype(self.ds.iloc[:, idx].dtype)  # type: ignore
        return None

    def sort(self, ncol: int, order):
        """
        override for AbstractitemModels
        Sort table by given column number.
        """
        if not self.do_sort:
            return None
        with self.change_layout():
            is_ascending = order == constants.ASCENDING
            self.ds = self.ds.sort_values(
                by=self.ds.columns[ncol], ascending=is_ascending
            )
            # method = datasetmethods.SortValuesMethod(
            #     by=self.ds.columns[ncol], ascending=is_ascending  # type: ignore
            # )
            # self.ds = method.apply_method(self.ds)  # type: ignore
        self.dataset_updated.emit(self.ds)


if __name__ == "__main__":

    app = widgets.app()
    view = widgets.TreeView()
    data = list(range(2000000))
    ds = pd.DataFrame(dict(a=[1, 2, 3], b=[1, 2, 3]))
    model = PandasModel(ds)
    view.set_model(model)
    view.show()
    app.main_loop()
