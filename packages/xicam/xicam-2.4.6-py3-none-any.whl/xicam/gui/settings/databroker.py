from collections import defaultdict
import os

from databroker import catalog, Broker
from databroker.utils import CONFIG_SEARCH_PATH
from qtpy.QtCore import Signal, Qt, QItemSelection
from qtpy.QtGui import QIcon, QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QAbstractItemView, QHBoxLayout, QLabel, QTreeView, QVBoxLayout, QWidget, QFrame

from xicam.core import threads, msg
from xicam.plugins.settingsplugin import SettingsPlugin
from xicam.gui import static


def find_catalog(catalog_name):
    # (adapted from databroker.utils.lookup_config)
    # Find catalog configuration file with the passed catalog name
    # returns the absolute file name for the configuration file
    if not catalog_name.endswith('.yml'):
        catalog_name += '.yml'
    for path in CONFIG_SEARCH_PATH:
        filename = os.path.join(path, catalog_name)
        if os.path.isfile(filename):
            return filename
    raise ValueError(f'Databroker found a config file named "{catalog_name}", but Xi-cam couldn\'t discover that same file.')

# TODO:
# - pick a better icon
# - add first column as representing checked/unchecked as a radio button
# - use selection model on view to enforce single selection of a broker

class BrokerModel(QStandardItemModel):
    """Qt standard item model that stores Brokers (which are Catalogs in databroker v2) in a tree hierarchy."""
    config_file_role = Qt.UserRole + 1
    catalog_role = Qt.UserRole + 2
    broker_role = catalog_role

    def __init__(self, *args, **kwargs):
        super(BrokerModel, self).__init__(*args, **kwargs)
        self.setHorizontalHeaderLabels(["Select a Broker for Run Engine to Use"])

    @threads.method()
    def add_catalogs(self):
        config_file_to_broker = defaultdict(list)
        catalog_names = list(catalog)

        for name in catalog_names:
            broker = Broker.named(name)
            if getattr(broker, 'v2', None) is None:
                msg.logMessage(f'The broker named {name} cannot be cast to a v2 Broker.', msg.WARNING)
                continue
            # catalog_dir might be in the metadata; if not, let's try to find it
            if 'catalog_dir' in broker.v2.metadata:
                config_file = broker.v2.metadata["catalog_dir"]
            else:
                config_file = find_catalog(name)

            config_file_to_broker[config_file].append(broker)

        for config_file, brokers in config_file_to_broker.items():
            config_file_item = QStandardItem()
            config_file_item.setData(config_file, Qt.DisplayRole)
            self.appendRow(config_file_item)
            for broker in brokers:
                broker_item = QStandardItem()
                broker_item.setData(broker.name, Qt.DisplayRole)
                broker_item.setData(broker, self.broker_role)
                config_file_item.appendRow(broker_item)


class BrokerView(QTreeView):
    """Tree-like view onto a list of Brokers.

    Each parent node is a directory, each child node is a Broker in the parent directory.

    Emits sigCurrentBrokerChanged anytime the current/active broker is changed in the view.
    """
    sigCurrentBrokerChanged = Signal(Broker)

    def __init__(self, parent=None):
        super(BrokerView, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._current_broker = None

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        selected_indexes = selected.indexes()
        if not selected_indexes:
            return
        data = selected_indexes[0].data(BrokerModel.broker_role)
        if data and data != self._current_broker:
            print(data)
            self._current_broker = data
            self.sigCurrentBrokerChanged.emit(data)

        super(BrokerView, self).selectionChanged(selected, deselected)


class DatabrokerSettingsPlugin(SettingsPlugin):
    """Settings plugin to configure a Broker for internal Xi-CAM RE instance."""
    def __init__(self):

        self._model = BrokerModel()
        self._model.add_catalogs()

        self._view = BrokerView()
        self._view.setModel(self._model)

        self._selected_broker = QLabel("(None)")
        self._selected_broker.setFrameStyle(QFrame.Box)

        def update_current_configuration_text(broker):
            self._selected_broker.setText(broker.name)

        self._view.sigCurrentBrokerChanged.connect(update_current_configuration_text)

        layout = QVBoxLayout()
        layout.addWidget(self._view)

        inner_layout = QHBoxLayout()
        label = QLabel("active broker:")
        label.setAlignment(Qt.AlignRight)
        inner_layout.addWidget(label)
        inner_layout.addWidget(self._selected_broker)

        layout.addLayout(inner_layout)

        self._widget = QWidget()
        self._widget.setLayout(layout)

        name = "Broker Configuration"
        icon = QIcon(static.path("icons/z.png"))
        super(DatabrokerSettingsPlugin, self).__init__(icon, name, self._widget)
        self.restore()
