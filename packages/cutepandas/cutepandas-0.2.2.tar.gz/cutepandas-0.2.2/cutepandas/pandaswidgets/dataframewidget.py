"""
@author: Philipp Temminghoff
"""

import logging

# import pandas as pd
from prettyqt import core, widgets

from processanalyzer import models
from processanalyzer.core import signals

# from processanalyzer.core.application import _
from processanalyzer.gui import basetableview, toolbars
from processanalyzer.util import debug

logger = logging.getLogger(__name__)


class DataFrameWidget(basetableview.BaseTableView):
    """
    Customized TableView class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSortingEnabled(True)
        self.v_header.hide()
        self.h_header.setSectionsMovable(False)
        # self.h_header.set_custom_menu(self.h_header_menu)

    def contextMenuEvent(self, event):
        """
        context menu override
        """
        if self.model() is None or self.model().is_read_only:
            event.accept()
            return None
        super().contextMenuEvent(event)

    def get_context(self):
        return dict(model=self.model(), indexes=self.selectedIndexes())

    # def h_header_menu(self, position):
    #     """
    #     context menu for the horizontal header
    #     """
    #     if self.model().is_read_only:
    #         return True
    #     col = self.h_header.logicalIndexAt(position.x())
    #     menu = widgets.Menu()
    #     action_remove_col = menu.addAction(_("Remove column"))
    #     is_multi = isinstance(self.model().ds.columns, pd.MultiIndex)
    #     action_stack = menu.addAction(_("Stack")) if is_multi else None
    #     action = menu.exec_(self.mapToGlobal(position))
    #     if action is None:
    #         return None
    #     if action == action_remove_col:
    #         self.model().removeColumn(col)
    #     if action == action_stack:
    #         self.model().stack()

    @core.Slot(object)
    @core.Slot(object, bool)
    @debug.timer
    def load(self, ds):
        if ds is None or ds.empty:
            self.set_model(None)
        else:
            model = models.PandasModel(ds)
            model.dataset_updated.connect(signals.signals.update_datasetmanager)
            model.dataset_updated.connect(signals.signals.update_indextree)
            model.dataset_updated.connect(signals.signals.update_featuretree)
            model.dataset_updated.connect(signals.signals.update_categorytree_ds)
            model.dataset_updated.connect(signals.signals.update_history)
            self.set_model(model)
            model.show_tooltips = True
            model.show_icons = True
            self.adapt_sizes()

    def set_ds(self, ds, read_only=False, color_values=False):
        if ds is not None:
            model = models.PandasModel(ds, read_only=read_only, color_values=color_values)
            self.set_model(model)
            self.adapt_sizes()
        else:
            self.set_model(None)


class ToolbarDataFrameWidget(widgets.Widget):
    def __init__(self, ds, read_only=True, parent=None):
        super().__init__(parent)
        v_layout = widgets.BoxLayout("vertical", self)
        table = DataFrameWidget()
        v_layout += table
        toolbar = toolbars.ToolBar()
        # action_export = toolbar.addAction(_("Export"))
        v_layout.setMenuBar(toolbar)
        table.set_ds(ds, read_only=read_only)


if __name__ == "__main__":
    app = widgets.app()
    from processanalyzer.core import dataset

    ds = dataset.DataSet(dict(a=list(range(100))))
    table = DataFrameWidget()
    table.set_ds(ds)
    table.show()
    table.adapt_sizes()
    app.main_loop()
