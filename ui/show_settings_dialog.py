# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLTools
                                 A QGIS plugin for the Ville de Lausanne
                              -------------------
        begin                : 2016-06-20
        git sha              : $Format:%H$
        copyright            : (C) 2016 Ville de Lausanne
        author               : Christophe Gusthiot
        email                : christophe.gusthiot@lausanne.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from PyQt4.QtGui import (QDialog,
                         QGridLayout,
                         QPushButton,
                         QLabel,
                         QComboBox)
from qgis.core import (QgsMapLayer,
                       QgsDataSourceURI,
                       QGis)
from ..core.db_connector import DBConnector


class ShowSettingsDialog(QDialog):
    def __init__(self, iface, memoryPointsLayer, memoryLinesLayer, configTable):
        QDialog.__init__(self)
        self.__iface = iface
        self.__memoryPointsLayer = memoryPointsLayer
        self.__memoryLinesLayer = memoryLinesLayer
        self.__configTable = configTable
        self.setWindowTitle("Settings")
        self.__pointsLayers = []
        self.__linesLayers = []
        self.__tables = []

        dataSource = QgsDataSourceURI(self.__layer.source())
        db = DBConnector.setConnection(dataSource.database(), self.__iface)
        if db:
            query = db.exec_("""SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN
                ('pg_catalog', 'information_schema', 'topology') AND table_type = 'BASE TABLE' AND table_name NOT IN
                (SELECT f_table_name FROM geometry_columns)""")
            while query.next():
                self.__tables.append(query.value(0))
            db.close()

        for layer in self.__iface.mapCanvas().layers():
            if layer is not None \
                and layer.type() == QgsMapLayer.VectorLayer \
                    and layer.providerType() == "memory":
                if layer.geometryType() == QGis.Point:
                    self.__pointsLayers.append(layer)
                if layer.geometryType() == QGis.Line:
                    self.__linesLayers.append(layer)
        self.resize(400, 200)
        self.__layout = QGridLayout()

        pointLabel = QLabel("Working points layer : ")
        pointLabel.setMinimumHeight(20)
        pointLabel.setMinimumWidth(50)
        self.__layout.addWidget(pointLabel, 0, 1)

        self.__pointCombo = QComboBox()
        self.__pointCombo.setMinimumHeight(20)
        self.__pointCombo.setMinimumWidth(50)
        self.__pointCombo.addItem("")
        for layer in self.__pointsLayers:
            self.__pointCombo.addItem(layer.name())
        self.__layout.addWidget(self.__pointCombo, 0, 2)
        self.__pointCombo.currentIndexChanged.connect(self.__pointComboChanged)
        if self.__memoryPointsLayer is not None:
            if self.__memoryPointsLayer in self.__pointsLayers:
                self.__pointCombo.setCurrentIndex(self.__pointsLayers.index(self.__memoryPointsLayer)+1)

        lineLabel = QLabel("Working lines layer : ")
        lineLabel.setMinimumHeight(20)
        lineLabel.setMinimumWidth(50)
        self.__layout.addWidget(lineLabel, 1, 1)

        self.__lineCombo = QComboBox()
        self.__lineCombo.setMinimumHeight(20)
        self.__lineCombo.setMinimumWidth(50)
        self.__lineCombo.addItem("")
        for layer in self.__linesLayers:
            self.__lineCombo.addItem(layer.name())
        self.__layout.addWidget(self.__lineCombo, 1, 2)
        self.__lineCombo.currentIndexChanged.connect(self.__lineComboChanged)
        if self.__memoryLinesLayer is not None:
            if self.__memoryLinesLayer in self.__linesLayers:
                self.__lineCombo.setCurrentIndex(self.__linesLayers.index(self.__memoryLinesLayer)+1)

        tableLabel = QLabel("Config table : ")
        tableLabel.setMinimumHeight(20)
        tableLabel.setMinimumWidth(50)
        self.__layout.addWidget(tableLabel, 2, 1)

        self.__tableCombo = QComboBox()
        self.__tableCombo.setMinimumHeight(20)
        self.__tableCombo.setMinimumWidth(50)
        self.__tableCombo.addItem("")
        for table in self.__tables:
            self.__tableCombo.addItem(table)
        self.__layout.addWidget(self.__tableCombo, 2, 2)
        self.__tableCombo.currentIndexChanged.connect(self.__tableComboChanged)
        if self.__configTable is not None:
            if self.__configTable in self.__tables:
                self.__tableCombo.setCurrentIndex(self.__tables.index(self.__configTable) + 1)

        self.__okButton = QPushButton("OK")
        self.__okButton.setMinimumHeight(20)
        self.__okButton.setMinimumWidth(100)

        self.__cancelButton = QPushButton("Cancel")
        self.__cancelButton.setMinimumHeight(20)
        self.__cancelButton.setMinimumWidth(100)

        self.__layout.addWidget(self.__okButton, 100, 1)
        self.__layout.addWidget(self.__cancelButton, 100, 2)
        self.setLayout(self.__layout)

    def __lineComboChanged(self):
        if self.__lineCombo.itemText(0) == "":
            self.__lineCombo.removeItem(0)

    def __pointComboChanged(self):
        if self.__pointCombo.itemText(0) == "":
            self.__pointCombo.removeItem(0)

    def __tableComboChanged(self):
        if self.__tableCombo.itemText(0) == "":
            self.__tableCombo.removeItem(0)

    def okButton(self):
        return self.__okButton

    def cancelButton(self):
        return self.__cancelButton

    def pointsLayer(self):
        index = self.__pointCombo.currentIndex()
        if self.__pointCombo.itemText(index) == "":
            return None
        else:
            return self.__pointsLayers[index]

    def linesLayer(self):
        index = self.__lineCombo.currentIndex()
        if self.__lineCombo.itemText(index) == "":
            return None
        else:
            return self.__linesLayers[index]

    def configTable(self):
        index = self.__tableCombo.currentIndex()
        if self.__tableCombo.itemText(index) == "":
            return None
        else:
            return self.__tables[index]
