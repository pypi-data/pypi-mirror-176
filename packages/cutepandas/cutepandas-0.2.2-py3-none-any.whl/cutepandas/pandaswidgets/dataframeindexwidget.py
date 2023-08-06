"""
@author: Philipp Temminghoff
"""

from prettyqt import core, widgets
from processanalyzer.gui import basetableview
from cutepandas.pandasmodels import pandasindexmodel


def _(label: str) -> str:
    return label


class DataFrameIndexWidget(basetableview.BaseTableView):
    """
    Customized TableView class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSortingEnabled(True)
        self.set_selection_behaviour("rows")

        self.set_vertical_scrollbar_policy("always_off")
        self.setMinimumWidth(5)

        self.v_header.hide()
        self.h_header.setSectionsMovable(False)
        self.h_header.set_custom_menu(self.h_header_menu)

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

    def h_header_menu(self, position):
        """
        context menu for the horizontal header
        """
        if self.model().is_read_only:
            return True
        col = self.h_header.logicalIndexAt(position.x())
        menu = widgets.Menu()
        act_remove_col = menu.addAction(_("Remove index"))
        action = menu.exec_(self.mapToGlobal(position))
        if action is None:
            return None
        if action == act_remove_col:
            self.model().removeColumn(col)

    @core.Slot(object)
    @core.Slot(object, bool)
    def load(self, ds, copy=False):
        if ds is None or ds.empty:
            self.set_model(None)
        else:
            model = pandasindexmodel.PandasIndexModel(ds)
            self.set_model(model)
            model.show_icons = True
            model.show_tooltips = True
            self.adapt_sizes()

    def set_ds(self, ds, read_only=False):
        if ds is not None:
            model = pandasindexmodel.PandasIndexModel(ds, read_only=read_only)
            self.set_model(model)
            self.adapt_sizes()
        else:
            self.set_model(None)


if __name__ == "__main__":
    app = widgets.app()
    import pandas as pd

    ds = pd.DataFrame(dict(a=list(range(100))))
    table = DataFrameIndexWidget()
    table.set_ds(ds)
    table.show()
    table.adapt_sizes()
    app.main_loop()
