'''
Created on Jan 21, 2013

@author: Nabori
'''

from PySide import QtCore, QtGui, QtDeclarative, QtUiTools
from PySide.QtCore import QObject #, pyqtSignal
from Character import Character, RefLists

from PySide.QtCore import Signal as pyqtSignal
from PySide.QtCore import Slot as pyqtSlot

import Races, Classes

uiDir = "..\UI"

#QtCore.pyqtSignal = QtCore.Signal
QtCore.pyqtSlot = QtCore.Slot

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.char = Character(self)

        self.initMenubar()
        self.setWindowTitle('Character Manager') 
        
        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        self.tabWidget = QtGui.QTabWidget()
        self.baseStatsWidget = BaseStatsWidget(self)
        self.curStatsWidget = CurrentStatsWidget(self)
        self.tabWidget.addTab(self.curStatsWidget.widget, "CurStats")
        
        self.inventLayout = InventoryLayout(self)
        self.tabWidget.addTab(self.inventLayout.widget, "Inventory")
        
        # add all main to the main vLayout
        self.mainLayout.addWidget(self.baseStatsWidget.widget)
        self.mainLayout.addWidget(self.tabWidget)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        
        self.updateDisplay()

    def updateDisplay(self):
        self.updateCharAbilities()
    
    def initMenubar(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save', self)
        #exitAction.setShortcut('Ctrl+Q')
        saveAction.setStatusTip('Save character to file')
        saveAction.triggered.connect(self.saveCharacter)

        loadAction = QtGui.QAction(QtGui.QIcon('load.png'), '&Load', self)
        #exitAction.setShortcut('Ctrl+Q')
        loadAction.setStatusTip('Load character from file')
        loadAction.triggered.connect(self.loadCharacter)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)

        
    def saveCharacter(self):
        fileName, filter = QtGui.QFileDialog.getSaveFileName(self, 'Save Dialog', r'C:\\')
        if(fileName):
            self.char.save(fileName)
             
    def loadCharacter(self):
        fileName, filter = QtGui.QFileDialog.getOpenFileName(self, 'Open Dialog', r'C:\\') 
        if(fileName):
            self.char.load(fileName)

    def addWidget(self, widget=None):
        if(widget):
            self.mainLayout.addWidget(widget)
#        else:
#            self.mainLayout.addWidget(Test())
            
    def changeItems(self):
        self.combo.clear()

    def valChanged(self):
        print "Value changed"
     
    def baseStrChanged(self):
        self.char.baseStr = self.baseStatsWidget.strVal

    def baseIntChanged(self):
        self.char.baseInt = self.baseStatsWidget.intVal

    def baseDexChanged(self):
        self.char.baseDex = self.baseStatsWidget.dexVal
    
    def baseConChanged(self):
        self.char.baseCon = self.baseStatsWidget.conVal
    
    def baseWisChanged(self):
        self.char.baseWis = self.baseStatsWidget.wisVal
    
    def baseChaChanged(self):
        self.char.baseCha = self.baseStatsWidget.chaVal

    def raceChanged(self):
        self.char.race = self.baseStatsWidget.race
        print "Race:" + self.baseStatsWidget.race
    
    def classChanged(self):
        print "Class:" + self.baseStatsWidget.classVal

    def updateCharAbilities(self):
        self.curStatsWidget.displayStrBonuses(self.char)
        self.curStatsWidget.displayIntBonuses(self.char)
        self.curStatsWidget.displayDexBonuses(self.char)
        self.curStatsWidget.displayConBonuses(self.char)
        self.curStatsWidget.displayWisBonuses(self.char)
        self.curStatsWidget.displayChaBonuses(self.char)
        
class CurrentStatsWidget(object):
    def __init__(self, parent):
        self.parent = parent
        
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(uiDir + "\characterCurrentStats.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file, self.parent)
        file.close()
        
        self.initFields()
    
    def initFields(self):
        # Stength fields
        self.strCurrent = self.widget.findChild(QtGui.QLabel, "str_current")
        self.strBendBars = self.widget.findChild(QtGui.QLabel, "str_bend_bars")
        self.strDmg = self.widget.findChild(QtGui.QLabel, "str_dmg")
        self.strHit = self.widget.findChild(QtGui.QLabel, "str_hit")
        self.strMaxPress = self.widget.findChild(QtGui.QLabel, "str_max_press")
        self.strOpenDoors = self.widget.findChild(QtGui.QLabel, "str_open_doors")
        self.strPercent = self.widget.findChild(QtGui.QLabel, "str_percent")
        self.strWtAll = self.widget.findChild(QtGui.QLabel, "str_wt_all")
    
        #Intelligence fields
        self.intCurrent = self.widget.findChild(QtGui.QLabel, "int_current")
        self.intNumLangs = self.widget.findChild(QtGui.QLabel, "int_num_langs")
        self.intMaxSplLvl = self.widget.findChild(QtGui.QLabel, "int_max_spell_lv")
        self.intToKnowSpl = self.widget.findChild(QtGui.QLabel, "int_to_know_spl")
        self.intMinKnownSpl = self.widget.findChild(QtGui.QLabel, "int_max_known_spl")
        self.intMaxKnownSpl = self.widget.findChild(QtGui.QLabel, "int_min_known_spl")
        self.intIllImm = self.widget.findChild(QtGui.QLabel, "int_ill_imm")
        
        #Dexterity fields
        self.dexCurrent = self.widget.findChild(QtGui.QLabel, "dex_current")
        self.dexACAdj = self.widget.findChild(QtGui.QLabel, "dex_ac_adj")
        self.dexDodgeAdj = self.widget.findChild(QtGui.QLabel, "dex_dodge_adj")
        self.dexMissileAdj = self.widget.findChild(QtGui.QLabel, "dex_missile_adj")
        self.dexReactAdj = self.widget.findChild(QtGui.QLabel, "dex_react_adj")

        #Constituion fields
        self.conCurrent = self.widget.findChild(QtGui.QLabel, "con_current")
        self.conHpAdj = self.widget.findChild(QtGui.QLabel, "con_ftr_hp_adj")
        self.conFtrHpAdj = self.widget.findChild(QtGui.QLabel, "con_hp_adj")
        self.conMaxNoRes = self.widget.findChild(QtGui.QLabel, "con_max_no_ress")
        self.conResSurv = self.widget.findChild(QtGui.QLabel, "con_reass_surv")
        self.conSysShock = self.widget.findChild(QtGui.QLabel, "con_system_shock")
        
        #Wisdom fields
        self.wisCurrent = self.widget.findChild(QtGui.QLabel, "wis_current")
        self.wisBonusSpl = self.widget.findChild(QtGui.QLabel, "wis_bonus_spl")
        self.wisMagDefAdj = self.widget.findChild(QtGui.QLabel, "wis_mag_def_adj")
        self.wisMaxSpLv = self.widget.findChild(QtGui.QLabel, "wis_max_spell_lv")
        self.wisSplFail = self.widget.findChild(QtGui.QLabel, "wis_spell_fail")

        #Charisma fields
        self.chaCurrent = self.widget.findChild(QtGui.QLabel, "cha_current")
        self.chaLoyalAdj = self.widget.findChild(QtGui.QLabel, "cha_loyal_adj")
        self.chaMaxNoHM = self.widget.findChild(QtGui.QLabel, "cha_max_no_hm")
        self.chaReacAdj = self.widget.findChild(QtGui.QLabel, "cha_reac_adj")
        

    def displayStrBonuses(self, charObj):
        self.strCurrent.setText(str(charObj.curStr))
        self.strHit.setText(str(charObj.toHitBonus))
        self.strDmg.setText(str(charObj.dmgBonus))
        self.strWtAll.setText(str(charObj.weightAllow))
        self.strMaxPress.setText(str(charObj.maxPress))
        self.strOpenDoors.setText(str(charObj.openDoors))
        self.strBendBars.setText(str(charObj.bendBars))
        self.strPercent.setText(str(charObj.strUnknownBonus))

    def displayIntBonuses(self, charObj):
        self.intCurrent.setText(str(charObj.curInt))
        self.intIllImm.setText(str(charObj.illImmunity))
        self.intMaxKnownSpl.setText(str(charObj.maxKnownSpells))
        self.intMaxSplLvl.setText(str(charObj.intMaxSpellLv))
        self.intNumLangs.setText(str(charObj.numLangs))
        self.intToKnowSpl.setText(str(charObj.knowSpell))
        self.intMinKnownSpl.setText(str(charObj.minKnownSpells))

    def displayDexBonuses(self, charObj):
        self.dexCurrent.setText(str(charObj.curDex))
        self.dexACAdj.setText(str(charObj.dexAcAdj))
        self.dexDodgeAdj.setText(str(charObj.dexDodgeAdj))
        self.dexMissileAdj.setText(str(charObj.dexMissleAsj))
        self.dexReactAdj.setText(str(charObj.dexReactAdj))

    def displayConBonuses(self, charObj):
        self.conCurrent.setText(str(charObj.curCon))
        self.conHpAdj.setText(str(charObj.hpAdj))
        self.conFtrHpAdj.setText(str(charObj.ftrHpAdj))
        self.conMaxNoRes.setText(str(charObj.maxNoRes))
        self.conResSurv.setText(str(charObj.resSurv))
        self.conSysShock.setText(str(charObj.sysShock))

    def displayWisBonuses(self, charObj):
        self.wisCurrent.setText(str(charObj.curWis))
        self.wisBonusSpl.setText(str(charObj.bonusSpl))
        self.wisMagDefAdj.setText(str(charObj.magDefAdj))
        self.wisMaxSpLv.setText(str(charObj.wisMaxSpellLv))
        self.wisSplFail.setText(str(charObj.splFail))
    
    def displayChaBonuses(self, charObj):
        self.chaCurrent.setText(str(charObj.curCha))
        self.chaLoyalAdj.setText(str(charObj.loyalAdj))
        self.chaMaxNoHM.setText(str(charObj.maxNoHM))
        self.chaReacAdj.setText(str(charObj.reacAdj))
        
class BaseStatsWidget(object):
    def __init__(self, parent):
        self.parent = parent
        
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(uiDir + "\characterBaseStats.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file, self.parent)
        file.close()

        self.initBaseAbilities()
        self.initCharacteristics()

    def initCharacteristics(self):
        self.nameWidget = self.widget.findChild(QtGui.QLineEdit, "name")
        self.raceWidget = self.widget.findChild(QtGui.QComboBox, "race")
        self.alignWidget = self.widget.findChild(QtGui.QComboBox, "alignment")
        self.classWidget = self.widget.findChild(QtGui.QComboBox, "char_class")
        self.levelWidget = self.widget.findChild(QtGui.QComboBox, "char_level")
        
        self.nameWidget.setText("TestName")
        
        self.raceWidget.clear()
        self.raceWidget.addItems([x.capitalize() for x in Races.races])
        
        self.classWidget.clear()
        self.classWidget.addItems([x.capitalize() for x in Classes.classes])
        
        lvls = self.parent.char.cls.possibleLevels
        self.levelWidget.addItems([str(x) for x in lvls])
        
        self.alignWidget.clear()
        self.alignWidget.addItems(RefLists.aligns)
    
        self.raceWidget.activated.connect(self.raceChange)
        self.classWidget.activated.connect(self.classChange)
        
        
    def initBaseAbilities(self):        
        self.strBase = self.widget.findChild(QtGui.QSpinBox, "str_base")
        self.intBase = self.widget.findChild(QtGui.QSpinBox, "int_base")
        self.dexBase = self.widget.findChild(QtGui.QSpinBox, "dex_base")
        self.conBase = self.widget.findChild(QtGui.QSpinBox, "con_base")
        self.wisBase = self.widget.findChild(QtGui.QSpinBox, "wis_base")
        self.chaBase = self.widget.findChild(QtGui.QSpinBox, "cha_base")
    
        self.strBase.valueChanged.connect(self.parent.baseStrChanged)
        self.intBase.valueChanged.connect(self.parent.baseIntChanged)
        self.dexBase.valueChanged.connect(self.parent.baseDexChanged)
        self.conBase.valueChanged.connect(self.parent.baseConChanged)
        self.wisBase.valueChanged.connect(self.parent.baseWisChanged)
        self.chaBase.valueChanged.connect(self.parent.baseChaChanged)
        
    @property
    def strVal(self):
        return self.strBase.value()

    @property
    def intVal(self):
        return self.intBase.value()

    @property
    def dexVal(self):
        return self.dexBase.value()

    @property
    def conVal(self):
        return self.conBase.value()

    @property
    def wisVal(self):
        return self.wisBase.value()

    @property
    def chaVal(self):
        return self.chaBase.value()
    
    @property
    def race(self):
        curI = self.raceWidget.currentIndex()
        return self.raceWidget.itemText(curI)

    @property
    def alignment(self):
        curI = self.alignWidget.currentIndex()
        return self.alignWidget.itemText(curI)

    @property
    def classVal(self):
        curI = self.classWidget.currentIndex()
        return self.classWidget.itemText(curI)
    
    def raceChange(self, val):
        self.parent.raceChanged()

    def classChange(self, val):
        self.parent.classChanged()

class InventoryLayout(object):
    def __init__(self, parent):
        self.parent = parent
        
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(uiDir + "\inventory.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file, self.parent)
        file.close()
        print self.widget
        
        layout = self.widget.findChild(QtGui.QHBoxLayout, "inventLayout")
        layout.addWidget(InventoryWidget(), 0, 0)
        layout.addWidget(InventoryWidget(),0, 1)

class InventoryWidget(QtGui.QTreeWidget):
    def __init__(self,*args,**kwargs):
        QtGui.QTreeWidget.__init__(self,*args,**kwargs)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setHeaderLabels(["Quantity", "Name", "Value", "Weight"])
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for i in xrange(5):
            item = QtGui.QTreeWidgetItem(self)
            item.setText(0, "Item - " + str(i))
            item.setText(1, str(i))
            item.setText(2, str(i*2))
            item.setText(3, str(i*3))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |
                            QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled) 

    def dropEvent(self, e):
        if(e.source() == self):
            print "Dragged to self"
        else:
            print "Dragged to other"
        
        QtGui.QTreeWidget.dropEvent(self,e)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
