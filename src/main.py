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

class GUI(object):
    def __init__(self):
        self.char = Character(self)
        self.main = MainWindow(control=self)
        self.initConnections()
        self.updateDisplayAll()
        
    def updateDisplayAll(self):
        self.updateCharAbilities()
        
    def updateCharAbilities(self):
        self.main.curStatsWidget.displayStrBonuses()
        self.main.curStatsWidget.displayIntBonuses()
        self.main.curStatsWidget.displayDexBonuses()
        self.main.curStatsWidget.displayConBonuses()
        self.main.curStatsWidget.displayWisBonuses()
        self.main.curStatsWidget.displayChaBonuses()
        self.main.curStatsWidget.displayHP()
                    
    def show(self):
        self.main.show()
    
    @property    
    def charName(self):
        return self.main.baseStatsWidget.name

    @charName.setter    
    def charName(self, val):
        self.main.baseStatsWidget.name = val

    @property    
    def race(self):
        return self.main.baseStatsWidget.race

    @race.setter
    def race(self, val):
        self.main.baseStatsWidget.race = val
        #self.main.curStatsWidget.updateDisplayAll()

    @property    
    def alignment(self):
        return self.main.baseStatsWidget.alignment

    @alignment.setter
    def alignment(self, val):
        self.main.baseStatsWidget.alignment = val

    @property    
    def cls(self):
        return self.main.baseStatsWidget.classVal
    
    @cls.setter
    def cls(self, val):
        self.main.baseStatsWidget.classVal = val
        #self.main.curStatsWidget.updateDisplayAll()
        
    @property
    def curLvl(self):
        return self.main.baseStatsWidget.curLvl
    
    @curLvl.setter
    def curLvl(self, val):
        self.main.baseStatsWidget.curLvl = val
        #self.main.curStatsWidget.updateDisplayAll()
        
    @property
    def lvlUpStats(self):
        return self.main.leveling.lvlUpStats()

    @lvlUpStats.setter
    def lvlUpStats(self, val):
        self.main.leveling.setLvlUpStats(val)
        #self.main.curStatsWidget.updateDisplayAll()
        
    def initConnections(self):
        # Base Vals
        self.main.baseStatsWidget.strBase.valueChanged.connect(self.baseStrUpdate)
        self.main.baseStatsWidget.intBase.valueChanged.connect(self.baseIntUpdate)
        self.main.baseStatsWidget.dexBase.valueChanged.connect(self.baseDexUpdate)
        self.main.baseStatsWidget.conBase.valueChanged.connect(self.baseConUpdate)
        self.main.baseStatsWidget.wisBase.valueChanged.connect(self.baseWisUpdate)
        self.main.baseStatsWidget.chaBase.valueChanged.connect(self.baseChaUpdate)
        self.main.baseStatsWidget.nameWidget.editingFinished.connect(self.nameUpdate)
        self.main.baseStatsWidget.raceWidget.currentIndexChanged.connect(self.raceUpdate)
        self.main.baseStatsWidget.classWidget.currentIndexChanged.connect(self.classUpdate)
        self.main.baseStatsWidget.alignWidget.currentIndexChanged.connect(self.alignUpdate)
        self.main.baseStatsWidget.levelWidget.currentIndexChanged.connect(self.levelUpdate)
        
        #Level stats
        self.main.leveling.signal.levelUpChange.connect(self.levelStatsUpdate)
        
        #CurStats
        self.main.curStatsWidget.hpInj.valueChanged.connect(self.injuryUpdate)
        
    def baseStrUpdate(self, val):
        self.char.updateBaseStr(val)
        self.main.curStatsWidget.updateDisplayAll()

    def baseIntUpdate(self, val):
        self.char.updateBaseInt(val)
        self.main.curStatsWidget.updateDisplayAll()

    def baseDexUpdate(self, val):
        self.char.updateBaseDex(val)
        self.main.curStatsWidget.updateDisplayAll()

    def baseConUpdate(self, val):
        self.char.updateBaseCon(val)
        self.main.curStatsWidget.updateDisplayAll()

    def baseWisUpdate(self, val):
        self.char.updateBaseWis(val)
        self.main.curStatsWidget.updateDisplayAll()

    def baseChaUpdate(self, val):
        self.char.updateBaseCha(val)
        self.main.curStatsWidget.updateDisplayAll()

    def nameUpdate(self, val):
        self.char.updateName(val)
        self.main.curStatsWidget.updateDisplayAll()

    def raceUpdate(self, val):
        self.char.updateRace(val)
        self.main.curStatsWidget.updateDisplayAll()

    def classUpdate(self, val):
        self.char.updateClass(val)
        self.main.curStatsWidget.updateDisplayAll()

    def alignUpdate(self, val):
        self.char.updateAlign(val)
        self.main.curStatsWidget.updateDisplayAll()

    def levelUpdate(self, val):
        self.char.updateLevel(val)
        self.main.curStatsWidget.updateDisplayAll()
        
    def levelStatsUpdate(self, val):
        self.char.updateLvlUpStats(val)
        self.main.curStatsWidget.updateDisplayAll()

    def injuryUpdate(self, val):
        self.char.updateInjury(val)
        self.main.curStatsWidget.displayHP()
    
    def setBaseStr(self, val):
        self.main.baseStatsWidget.strBase.setValue(val)

    def setBaseInt(self, val):
        self.main.baseStatsWidget.intBase.setValue(val)

    def setBaseDex(self, val):
        self.main.baseStatsWidget.dexBase.setValue(val)

    def setBaseCon(self, val):
        self.main.baseStatsWidget.conBase.setValue(val)

    def setBaseWis(self, val):
        self.main.baseStatsWidget.wisBase.setValue(val)

    def setBaseCha(self, val):
        self.main.baseStatsWidget.chaBase.setValue(val)
    
    def setInjury(self, val):
        self.main.curStatsWidget.hpInj.setValue(val)
        
class UpdateManager(object):
    def __init__(self, main, base, current, leveling = None):
        self.main = main
        self.base = base
        self.current = current
        self.leveling = leveling

class LevelStatsUpdateSignal(QtCore.QObject):
    levelUpChange = QtCore.Signal(list)
    
class LevelingWindow(QtGui.QWidget):
    
    def __init__(self, parent = None):
        super(LevelingWindow, self).__init__(parent)
        
        self.signal = LevelStatsUpdateSignal()
        
        self.parent = parent
        
        self.grid = QtGui.QGridLayout()
        
        label = QtGui.QLabel()
        label.setText("Level")
        self.grid.addWidget(label, 0, 0)

        label = QtGui.QLabel()
        label.setText("HP Rolls")
        self.grid.addWidget(label, 0, 1)
        
        self.hpRollWidgets = []
        for i in xrange(1, 21):
            label = QtGui.QLabel()
            label.setText("Level {0}".format(i))
            self.grid.addWidget(label, i, 0)
            
            widget = QtGui.QLineEdit()
            widget.editingFinished.connect(self.lvlUpChange)
            self.hpRollWidgets.append(widget)
            self.grid.addWidget(widget, i, 1)
                
        self.setLayout(self.grid)
    
    def initCharacteristics(self):
        self.grid = self.widget.findChild(QtGui.QVBoxLayout, "lvlUpBox")
        #self.grid.setContentsMargins(0)
        self.addNewRow()
        
    def lvlUpStats(self):
        maxDim = max([len(self.hpRollWidgets) - 1])
        
        lvlUps = [[i+1, None] for i in range(maxDim)]
        
        for i in range(len(self.hpRollWidgets)-1):
            lvlUps[i][1] = self.hpRollWidgets[i].text()
        return lvlUps
    
    def setLvlUpStats(self, val):
        for i in range(len(val)):
            self.hpRollWidgets[i].setText(val[i])
        for i in range(len(val), len(self.hpRollWidgets)):
            self.hpRollWidgets[i].clear()
    
    def lvlUpChange(self):
        if(self.hpRollWidgets[-1].text()):
            self.addNewRow()
        #TODO: Validate the 
        self.signal.levelUpChange.emit(self.lvlUpStats())
        #self.parent.char.updateLvlUpStats(self.lvlUpStats())
        
    def addNewRow(self):
        nRows = len(self.hpRollWidgets)
        
        nextLvl = nRows+1
        
        lvlLabel = QtGui.QLabel()
        #lvlLabel.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        lvlLabel.setText("Lvl {0}".format(nextLvl))
        
        lvlRoll = QtGui.QLineEdit()
        #lvlRoll.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        lvlRoll.editingFinished.connect(self.lvlUpChange)
        self.hpRollWidgets.append(lvlRoll)
        
        newRow = QtGui.QHBoxLayout()
        newRow.addWidget(lvlLabel)
        newRow.addWidget(lvlRoll)
        self.grid.insertLayout(nextLvl, newRow)
        
    def getTotalHpRolls(self):
        hpRolls = filter(None, [x.text() for x in self.hpRollWidgets])
        return sum([int(x) for x in hpRolls])
        
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None, control=None):
        super(MainWindow, self).__init__(parent)
        self.control = control
        
        self.setMinimumSize(1000, 800)
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

        self.leveling = LevelingWindow(self)
        self.tabWidget.addTab(self.leveling, "Levelling")
        
        # add all main to the main vLayout
        self.mainLayout.addWidget(self.baseStatsWidget.widget)
        self.mainLayout.addWidget(self.tabWidget)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        
    @property
    def char(self):
        return self.control.char

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

#        levelWinAction = QtGui.QAction(QtGui.QIcon('load.png'), '&Level', self)
#        levelWinAction.setStatusTip('Open levelling window')
#        levelWinAction.triggered.connect(self.loadLevelingWindow)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
#        otherMenu = menubar.addMenu('&Other')
#        otherMenu.addAction(levelWinAction)

#    def loadLevelingWindow(self):
#        self.lvlWindow = LevelingWindow(self)
#        self.lvlWindow.show()
    
    def saveCharacter(self):
        fileName, filter = QtGui.QFileDialog.getSaveFileName(self, 'Save Dialog', r'C:\\')
        if(fileName):
            self.char.save(fileName)
             
    def loadCharacter(self):
        fileName, filter = QtGui.QFileDialog.getOpenFileName(self, 'Open Dialog', r'C:\\') 
        if(fileName):
            self.char.load(fileName)

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
        
        # HP fields
        self.hpMax = self.widget.findChild(QtGui.QLabel, "hp_max")
        self.hpInj = self.widget.findChild(QtGui.QSpinBox, "hp_injury")
        self.hpCur = self.widget.findChild(QtGui.QLabel, "hp_cur")
        #self.hpInj.valueChanged.connect(self.displayHP)
        
    def displayStrBonuses(self):
        charObj = self.parent.char
        self.strCurrent.setText(str(charObj.curStr))
        self.strHit.setText(str(charObj.toHitBonus))
        self.strDmg.setText(str(charObj.dmgBonus))
        self.strWtAll.setText(str(charObj.weightAllow))
        self.strMaxPress.setText(str(charObj.maxPress))
        self.strOpenDoors.setText(str(charObj.openDoors))
        self.strBendBars.setText(str(charObj.bendBars))
        self.strPercent.setText(str(charObj.strUnknownBonus))

    def displayIntBonuses(self):
        charObj = self.parent.char
        self.intCurrent.setText(str(charObj.curInt))
        self.intIllImm.setText(str(charObj.illImmunity))
        self.intMaxKnownSpl.setText(str(charObj.maxKnownSpells))
        self.intMaxSplLvl.setText(str(charObj.intMaxSpellLv))
        self.intNumLangs.setText(str(charObj.numLangs))
        self.intToKnowSpl.setText(str(charObj.knowSpell))
        self.intMinKnownSpl.setText(str(charObj.minKnownSpells))

    def displayDexBonuses(self):
        charObj = self.parent.char
        self.dexCurrent.setText(str(charObj.curDex))
        self.dexACAdj.setText(str(charObj.dexAcAdj))
        self.dexDodgeAdj.setText(str(charObj.dexDodgeAdj))
        self.dexMissileAdj.setText(str(charObj.dexMissleAsj))
        self.dexReactAdj.setText(str(charObj.dexReactAdj))

    def displayConBonuses(self):
        charObj = self.parent.char
        self.conCurrent.setText(str(charObj.curCon))
        self.conHpAdj.setText(str(charObj.hpAdj))
        self.conFtrHpAdj.setText(str(charObj.ftrHpAdj))
        self.conMaxNoRes.setText(str(charObj.maxNoRes))
        self.conResSurv.setText(str(charObj.resSurv))
        self.conSysShock.setText(str(charObj.sysShock))

    def displayWisBonuses(self):
        charObj = self.parent.char
        self.wisCurrent.setText(str(charObj.curWis))
        self.wisBonusSpl.setText(str(charObj.bonusSpl))
        self.wisMagDefAdj.setText(str(charObj.magDefAdj))
        self.wisMaxSpLv.setText(str(charObj.wisMaxSpellLv))
        self.wisSplFail.setText(str(charObj.splFail))
    
    def displayChaBonuses(self):
        charObj = self.parent.char
        self.chaCurrent.setText(str(charObj.curCha))
        self.chaLoyalAdj.setText(str(charObj.loyalAdj))
        self.chaMaxNoHM.setText(str(charObj.maxNoHM))
        self.chaReacAdj.setText(str(charObj.reacAdj))
    
    def displayHP(self):
        charObj = self.parent.char
        self.hpMax.setText(str(charObj.maxHP))
        inj = charObj.injury
        self.hpCur.setText(str(charObj.maxHP-inj))

    def updateDisplayAll(self):
        self.displayStrBonuses()
        self.displayIntBonuses()    
        self.displayDexBonuses()
        self.displayConBonuses()
        self.displayWisBonuses()
        self.displayChaBonuses()
        self.displayHP()
        
        
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
        self.xpToNextLvlWidget = self.widget.findChild(QtGui.QLabel, "char_xp_to_next_lvl")
        
        self.raceWidget.clear()
        self.raceWidget.addItems([x.capitalize() for x in Races.races])
        
        self.classWidget.clear()
        self.classWidget.addItems([x.capitalize() for x in Classes.classes])
        
        lvls = self.parent.char.cls.possibleLevels
        self.levelWidget.addItems([str(x) for x in lvls])

        curLvl = self.levelWidget.currentText()
        nextLvlXP = self.parent.char.cls.xpForLvl(curLvl)
        self.xpToNextLvlWidget.setText(str(nextLvlXP))
             
        self.alignWidget.clear()
        self.alignWidget.addItems(RefLists.aligns)
    
#        self.nameWidget.editingFinished.connect(self.parent.char.updateName)
#        self.raceWidget.activated.connect(self.parent.char.updateRace)
#        self.classWidget.activated.connect(self.parent.char.updateClass)
#        self.alignWidget.activated.connect(self.parent.char.updateAlign)
#        self.levelWidget.activated.connect(self.parent.char.updateLevel)
        
    def initBaseAbilities(self):        
        self.strBase = self.widget.findChild(QtGui.QSpinBox, "str_base")
        self.intBase = self.widget.findChild(QtGui.QSpinBox, "int_base")
        self.dexBase = self.widget.findChild(QtGui.QSpinBox, "dex_base")
        self.conBase = self.widget.findChild(QtGui.QSpinBox, "con_base")
        self.wisBase = self.widget.findChild(QtGui.QSpinBox, "wis_base")
        self.chaBase = self.widget.findChild(QtGui.QSpinBox, "cha_base")
    
#        self.strBase.valueChanged.connect(self.parent.char.updateBaseStr)
#        self.intBase.valueChanged.connect(self.parent.char.updateBaseInt)
#        self.dexBase.valueChanged.connect(self.parent.char.updateBaseDex)
#        self.conBase.valueChanged.connect(self.parent.char.updateBaseCon)
#        self.wisBase.valueChanged.connect(self.parent.char.updateBaseWis)
#        self.chaBase.valueChanged.connect(self.parent.char.updateBaseCha)
        
    @property
    def strVal(self):
        return self.strBase.value()
    
    @strVal.setter
    def strVal(self, val):
        self.strBase.setValue(val)

    @property
    def intVal(self):
        return self.intBase.value()

    @intVal.setter
    def intVal(self, val):
        self.intBase.setValue(val)

    @property
    def dexVal(self):
        return self.dexBase.value()

    @dexVal.setter
    def dexVal(self, val):
        self.dexBase.setValue(val)

    @property
    def conVal(self):
        return self.conBase.value()

    @conVal.setter
    def conVal(self, val):
        self.conBase.setValue(val)

    @property
    def wisVal(self):
        return self.wisBase.value()

    @wisVal.setter
    def wisVal(self, val):
        self.wisBase.setValue(val)

    @property
    def chaVal(self):
        return self.chaBase.value()

    @chaVal.setter
    def chaVal(self, val):
        self.chaBase.setValue(val)
    
    @property
    def name(self):
        return self.nameWidget.text()
    
    @name.setter
    def name(self, val):
        self.nameWidget.setText(val)

    @property
    def race(self):
        curI = self.raceWidget.currentIndex()
        return self.raceWidget.itemText(curI)

    @race.setter
    def race(self, val):
        i = self.raceWidget.findText(val, QtCore.Qt.MatchFixedString)
        self.raceWidget.setCurrentIndex(i)

    @property
    def alignment(self):
        curI = self.alignWidget.currentIndex()
        return self.alignWidget.itemText(curI)

    @alignment.setter
    def alignment(self, val):
        i = self.alignWidget.findText(val, QtCore.Qt.MatchFixedString)
        self.alignWidget.setCurrentIndex(i)

    @property
    def classVal(self):
        curI = self.classWidget.currentIndex()
        return self.classWidget.itemText(curI)

    @classVal.setter
    def classVal(self, val):
        i = self.classWidget.findText(val, QtCore.Qt.MatchFixedString)
        self.classWidget.setCurrentIndex(i)

    @property
    def curLvl(self):
        return self.levelWidget.currentText()

    @curLvl.setter
    def curLvl(self, val):
        i = self.levelWidget.findText(str(val), QtCore.Qt.MatchContains)
        self.levelWidget.setCurrentIndex(i)
    
class InventoryLayout(object):
    def __init__(self, parent):
        self.parent = parent
        
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(uiDir + "\inventory.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file, self.parent)
        file.close()
        
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
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
