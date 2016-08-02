# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLTools
                                 A QGIS plugin for the Ville de Lausanne
                              -------------------
        begin                : 2016-07-18
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

from PyQt4.QtCore import QSettings
from PyQt4.QtSql import QSqlDatabase
from qgis.gui import QgsMessageBar


class DBConnector:

    @staticmethod
    def getDefault(dataSource, db):
        query_string = """SELECT column_default FROM information_schema.columns WHERE table_name='""" + \
                       dataSource.table() + """' AND column_name='""" + dataSource.keyColumn() + """'"""
        print(query_string)
        query = db.exec_(query_string)
        print("num", query.size())
        while query.next():
            print("query", query.value(0))
            return query.value(0)
        return None

    @staticmethod
    def getConnections():
        s = QSettings()
        s.beginGroup("PostgreSQL/connections")
        currentConnections = s.childGroups()
        s.endGroup()
        return currentConnections

    @staticmethod
    def setConnection(conn, iface):
        s = QSettings()
        s.beginGroup("PostgreSQL/connections/" + conn)
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(s.value("host", ""))
        db.setDatabaseName(s.value("database", ""))
        db.setUserName(s.value("username", ""))
        db.setPassword(s.value("password", ""))
        s.endGroup()
        ok = db.open()
        if not ok:
            iface.messageBar().pushMessage("Database Error: " + db.lastError().text(), level=QgsMessageBar.CRITICAL)
            return None
        return db