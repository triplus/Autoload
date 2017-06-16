# AutoLoad module for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Autoload module for FreeCAD."""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/Autoload")
g = App.ParamGet("User parameter:BaseApp/Preferences/General")


def wbIcon(i):
    """Create workbench icon."""
    if str(i.find("XPM")) != "-1":
        icon = []
        for a in ((((i
                     .split('{', 1)[1])
                    .rsplit('}', 1)[0])
                   .strip())
                  .split("\n")):
            icon.append((a
                         .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        icon = QtGui.QIcon(QtGui.QPixmap(icon))
    else:
        icon = QtGui.QIcon(QtGui.QPixmap(i))
    if icon.isNull():
        icon = QtGui.QIcon(":/icons/freecad")
    return icon


def widget():
    """Create autoload preferences dialog."""
    w = QtGui.QListWidget()
    mod = p.GetString("modules")
    mod = mod.split(",")
    wb = Gui.listWorkbenches()
    wbSort = list(wb)
    wbSort.sort()
    default = g.GetString("AutoloadModule", "StartWorkbench")

    for i in wbSort:
        name = wb[i].__class__.__name__
        item = QtGui.QListWidgetItem(w)
        item.setText(wb[i].MenuText)
        item.setData(32, name)
        try:
            icon = wbIcon(wb[i].Icon)
        except:
            icon = QtGui.QIcon(":/icons/freecad")
        item.setIcon(icon)
        if name == default:
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            item.setCheckState(QtCore.Qt.CheckState(2))
        elif name in mod:
            item.setCheckState(QtCore.Qt.CheckState(2))
        else:
            item.setCheckState(QtCore.Qt.CheckState(0))

    def onList():
        """Save changes."""
        items = []
        for index in range(w.count()):
            if w.item(index).checkState() == QtCore.Qt.Checked:
                items.append(w.item(index).data(32))
        p.SetString("modules", ",".join(items))

    w.itemChanged.connect(onList)
    return w


def preferencesDialog():
    """Preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dia.done(1)

    def onFinished():
        """Delete dialog on close."""
        dia.deleteLater()

    dia = QtGui.QDialog(mw)
    dia.resize(800, 450)
    dia.setWindowTitle("Autoload")
    dia.setObjectName("Autoload")
    lo = QtGui.QVBoxLayout()
    dia.setLayout(lo)
    btnCl = QtGui.QPushButton("Close", dia)
    btnCl.setDefault(True)
    loCl = QtGui.QHBoxLayout()
    loCl.addStretch(1)
    loCl.addWidget(btnCl)
    w = widget()
    w.setParent(dia)
    lo.addWidget(w)
    lo.insertLayout(1, loCl)
    dia.finished.connect(onFinished)
    btnCl.clicked.connect(onAccepted)
    return dia


def onPreferences():
    """Open the preferences dialog."""
    dia = preferencesDialog()
    dia.show()


def accessoriesMenu():
    """Add autoload preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Autoload")
    pref.setObjectName("Autoload")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("Autoload")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu()
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")
                if toolsMenu:
                    toolsMenu.addAction(action)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def loadModules():
    """Load modules"""
    wb = Gui.listWorkbenches()
    mod = p.GetString("modules")
    mod = mod.split(",")
    default = g.GetString("AutoloadModule", "StartWorkbench")
    for i in mod:
        if i in wb and i != default:
            Gui.activateWorkbench(i)
    if default in mod:
        Gui.activateWorkbench(default)


def onStart():
    """Start autoload."""
    start = False
    try:
        mw.workbenchActivated
        start = True
    except AttributeError:
        pass
    if start:
        timer.stop()
        timer.deleteLater()
        loadModules()
        accessoriesMenu()


timer = QtCore.QTimer()
timer.timeout.connect(onStart)
timer.start(500)
