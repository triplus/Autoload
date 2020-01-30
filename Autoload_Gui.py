# AutoLoad module for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017, 2018, 2019 triplus @ FreeCAD
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

import os
import importlib
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/Autoload")
pGen = App.ParamGet("User parameter:BaseApp/Preferences/General")
default = pGen.GetString("AutoloadModule", "StartWorkbench")
defaultPath = App.getUserAppDataDir() + "Macro"
customPath = App.ParamGet('User parameter:BaseApp/Preferences/Macro')
path = customPath.GetString("MacroPath", defaultPath)


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


def modules():
    """Available modules in the macro folder."""
    mod = []
    if os.path.isdir(path):
        for i in os.listdir(path):
            if (os.path.isfile(path + os.sep + i) and
                    i.startswith("Autoload_") and
                    i.endswith(".py")):
                mod.append(i)
    return mod


def widget(dia):
    """List widget for autoload preferences dialog."""
    w = QtGui.QListWidget(dia)
    mod = p.GetString("modules")
    mod = mod.split(",")
    available = modules()
    wb = Gui.listWorkbenches()
    wbSort = list(wb)
    wbSort.sort()
    for i in available:
        item = QtGui.QListWidgetItem(w)
        if i.startswith("Autoload_1_"):
            item.setText(i[11:][:-3] + " (Custom)")
        else:
            item.setText(i[9:][:-3] + " (Custom)")
        item.setData(32, i)
        item.setIcon(QtGui.QIcon(":/icons/freecad"))
        if i in mod:
            item.setCheckState(QtCore.Qt.CheckState(2))
        else:
            item.setCheckState(QtCore.Qt.CheckState(0))
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
    w = widget(dia)
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
    pref.setText("Autoload...")
    pref.setObjectName("Autoload")
    pref.setStatusTip("Load specified workbenches and macros on startup")
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
                mb.addAction(action)
                action.setVisible(True)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def loadModulesFirst():
    """Load modules on Autoload init."""
    mod = p.GetString("modules")
    mod = mod.split(",")
    for i in mod:
        try:
            if (os.path.isfile(path + os.sep + i) and
                    i.startswith("Autoload_") and not
                    i.startswith("Autoload_1_")):
                importlib.import_module(i[:-3])
        except Exception as e:
            print("Autoload: Exception in " + i + " of type " + str(e))


def loadWorkbenches():
    """Load workbenches."""
    wb = Gui.listWorkbenches()
    mod = p.GetString("modules")
    mod = mod.split(",")
    for i in mod:
        if i in wb and i != default:
            Gui.activateWorkbench(i)
    if default in mod:
        Gui.activateWorkbench(default)


def loadModulesLast():
    """Load modules at latter start stage."""
    mod = p.GetString("modules")
    mod = mod.split(",")
    for i in mod:
        try:
            if (os.path.isfile(path + os.sep + i) and
                    i.startswith("Autoload_1_")):
                importlib.import_module(i[:-3])
        except Exception as e:
            print("Autoload: Exception in " + i + " of type " + str(e))


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
        accessoriesMenu()
        loadWorkbenches()
        loadModulesLast()


def onPreStart():
    """Improve start reliability and maintain FreeCAD 0.16 support."""
    if App.Version()[1] < "17":
        onStart()
    else:
        if mw.property("eventLoop"):
            onStart()


loadModulesFirst()
timer = QtCore.QTimer()
timer.timeout.connect(onPreStart)
timer.start(500)
