'''
Created on Jan 21, 2013

@author: Nabori
'''

from Abilities import StrTab, IntTab, ConTab, DexTab, WisTab, ChaTab, Abilities
from Races import Race, Human
from Classes import Class
from xml.dom.minidom import Document, parse

import xml.parsers.expat
import xml.dom
import os
import itertools

class RefLists():
    order = ["Lawful", "Neutral", "Chaotic"]
    morality = ["Good", "Neutral", "Evil"]
    aligns = map("-".join, itertools.product(order, morality))
    
class GUICharacterSlots(object):
    def updateBaseStr(self, val):
        self.baseStr = val
    
    def updateBaseInt(self, val):
        self.baseInt = val
    
    def updateBaseWis(self, val):
        self.baseWis = val

    def updateBaseDex(self, val):
        self.baseDex = val

    def updateBaseCon(self, val):
        self.baseCon = val

    def updateBaseCha(self, val):
        self.baseCha = val
        
    def updateName(self):
        self.name = self._guiObj.charName
    
    def updateRace(self, val):
        self.race = self._guiObj.race
    
    def updateClass(self, val):
        self.cls = self._guiObj.cls

    def updateAlign(self, val):
        self.alignment = self._guiObj.alignment

    def updateLevel(self, val):
        self.lvlUps = self._guiObj.lvlUpStats

    def updateXP(self, val):
        #TODO: Enable XP saving
        print "Do something for XP {}".format(val)

    def updateLvlUpStats(self, stats):
        self.lvlUps = stats
        
    def updateInjury(self, val):
        self.injury = val
    
    
class Character(GUICharacterSlots):
    '''
    
    '''

    def __init__(self, guiObj):
        '''
        '''
        self.savedata = CharSaveData(None)
        
#        self.baseAbilites = {}
#        for x in Abilities.fullList:
#            self.baseAbilites[x] = 3
        
        self._strTab = StrTab()
        self._intTab = IntTab()
        self._conTab = ConTab()
        self._dexTab = DexTab()
        self._wisTab = WisTab()
        self._chaTab = ChaTab()
        
        self._guiObj = guiObj
        
        self._race = Race.createRace("human")
        
        self._class = Class.createClass("fighter")
    
    def save(self, fileName):
        self.savedata.save(fileName)

    def load(self, fileName):
        #TODO: Fix loading
        self.savedata = CharSaveData(fileName)
        
        self._guiObj.charName = self.savedata.name
        self._guiObj.alignment = self.savedata.align
        self._guiObj.cls = self.savedata.charClass
        self._guiObj.race = self.savedata.race
        self._guiObj.lvlUpStats = self.lvlUps
        self._guiObj.curLvl = self.savedata.level

        self._guiObj.setBaseStr(self.baseStr)
        self._guiObj.setBaseInt(self.baseInt)
        self._guiObj.setBaseDex(self.baseDex)
        self._guiObj.setBaseWis(self.baseWis)
        self._guiObj.setBaseCon(self.baseCon)
        self._guiObj.setBaseCha(self.baseCha)
        
        self._guiObj.setInjury(self.injury)
        
        self._guiObj.updateCharAbilities()
#        self._guiObj.baseStrChanged(self.baseStr)
#        self._guiObj.baseIntChanged(self.baseInt)
#        self._guiObj.baseDexChanged(self.baseDex)
#        self._guiObj.baseConChanged(self.baseCon)
#        self._guiObj.baseWisChanged(self.baseWis)
#        self._guiObj.baseChaChanged(self.baseCha)
        
        #TODO: Load leveling up stats
    
    @property
    def race(self):
        return self._race
            
    @race.setter
    def race(self, val):
        self._race = Race.createRace(val)
        self.savedata.race = self._race
        self._guiObj.updateCharAbilities()

    @property
    def cls(self):
        return self._class
    
    @cls.setter
    def cls(self, val):
        self._class = Class.createClass(val)
        self.savedata.charClass = self._class
        self._guiObj.updateCharAbilities()
        
    @property
    def alignment(self):
        return self.savedata.align
    
    @alignment.setter
    def alignment(self, val):
        self.savedata.align = val
        
    @property
    def lvlUps(self):
        return self.savedata.lvlUps
    
    @lvlUps.setter
    def lvlUps(self, val):
        lvl = self._guiObj.curLvl
        lvl = lvl[0:lvl.find(" ")]
        lvls = val[0:int(lvl)]
        self.savedata.lvlUps = lvls
        self.savedata.level = len(lvls)
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        self.savedata.name = val

    @property
    def maxHP(self):
        hp = 10
        upgrades = self.lvlUps
        for x in upgrades:
            try:
                hp += int(x)
            except ValueError:
                pass #print "Invalid HP Roll"
            hp += self.cls.hpBonusPerLvl
            
        return hp
    
    @property
    def injury(self):
        return self.savedata.injury
    
    @injury.setter
    def injury(self, val):
        self.savedata.injury = val
        
    @property
    def baseStr(self):
        return self.savedata.strength
        #return self.baseAbilites[Abilities.strStr]

    @baseStr.setter
    def baseStr(self, val):
        self.savedata.strength = val
        #self.baseAbilites[Abilities.strStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curStr(self):
        val = self.baseStr
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.strStr in raceBonus):
            val += raceBonus[Abilities.strStr]
        return val

    @property
    def toHitBonus(self):
        val = self._strTab.toHitBonus(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def dmgBonus(self):
        val = self._strTab.dmgBonus(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def weightAllow(self):
        val = self._strTab.weightAllow(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def maxPress(self):
        val = self._strTab.maxPress(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def openDoors(self):
        val = self._strTab.openDoors(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def bendBars(self):
        val = self._strTab.bendBars(self.curStr)
        # Apply bonuses (race, other?)
        return val

    @property
    def strUnknownBonus(self):
        val = self._strTab.unknownBonus(self.curStr)
        # Apply bonuses (race, other?)
        return val
        
    @property
    def baseInt(self):
        return self.savedata.intel
        #return self.baseAbilites[Abilities.intStr]

    @baseInt.setter
    def baseInt(self, val):
        self.savedata.intel = val
        #self.baseAbilites[Abilities.intStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curInt(self):
        val = self.baseInt
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.intStr in raceBonus):
            val += raceBonus[Abilities.intStr]

        return val

    @property
    def illImmunity(self):
        val = self._intTab.illImmunity(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def maxKnownSpells(self):
        val = self._intTab.maxKnownSpells(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def intMaxSpellLv(self):
        val = self._intTab.maxSpellLv(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def numLangs(self):
        val = self._intTab.numLangs(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def knowSpell(self):
        val = self._intTab.knowSpell(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def minKnownSpells(self):
        val = self._intTab.minKnownSpells(self.curInt)
        # Apply bonuses (race, other?)
        return val

    @property
    def baseCon(self):
        return self.savedata.con
        #return self.baseAbilites[Abilities.conStr]

    @baseCon.setter
    def baseCon(self, val):
        self.savedata.con = val
        #self.baseAbilites[Abilities.conStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curCon(self):
        val = self.baseCon
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.conStr in raceBonus):
            val += raceBonus[Abilities.conStr]
        return val

    @property
    def hpAdj(self):
        val = self._conTab.hpBonus(self.curCon)
        # Apply bonuses (race, other?)
        return val

    @property
    def ftrHpAdj(self):
        val = self._conTab.hpfBonus(self.curCon)
        # Apply bonuses (race, other?)
        return val

    @property
    def maxNoRes(self):
        val = self._conTab.NR(self.curCon)
        # Apply bonuses (race, other?)
        return val

    @property
    def resSurv(self):
        val = self._conTab.res(self.curCon)
        # Apply bonuses (race, other?)
        return val

    @property
    def sysShock(self):
        val = self._conTab.shock(self.curCon)
        # Apply bonuses (race, other?)
        return val

    @property
    def baseDex(self):
        return self.savedata.dex
        #return self.baseAbilites[Abilities.dexStr]

    @baseDex.setter
    def baseDex(self, val):
        self.savedata.dex = val
        #self.baseAbilites[Abilities.dexStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curDex(self):
        val = self.baseDex
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.dexStr in raceBonus):
            val += raceBonus[Abilities.dexStr]

        return val

    @property
    def dexAcAdj(self):
        val = self._dexTab.acAdj(self.curDex)
        # Apply bonuses (race, other?)
        return val

    @property
    def dexDodgeAdj(self):
        val = self._dexTab.dodgeAdj(self.curDex)
        # Apply bonuses (race, other?)
        return val

    @property
    def dexMissleAsj(self):
        val = self._dexTab.missleAdj(self.curDex)
        # Apply bonuses (race, other?)
        return val

    @property
    def dexReactAdj(self):
        val = self._dexTab.reactAdj(self.curDex)
        # Apply bonuses (race, other?)
        return val

    @property
    def baseWis(self):
        return self.savedata.wis
        #return self.baseAbilites[Abilities.wisStr]

    @baseWis.setter
    def baseWis(self, val):
        self.savedata.wis = val
        #self.baseAbilites[Abilities.wisStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curWis(self):
        val = self.baseWis
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.wisStr in raceBonus):
            val += raceBonus[Abilities.wisStr]
        return val

    @property
    def bonusSpl(self):
        val = self._wisTab.bonusSpells(self.curWis)
        # Apply bonuses (race, other?)
        return val

    @property
    def magDefAdj(self):
        val = self._wisTab.magDefAdj(self.curWis)
        # Apply bonuses (race, other?)
        return val

    @property
    def wisMaxSpellLv(self):
        val = self._wisTab.maxSpellLv(self.curWis)
        # Apply bonuses (race, other?)
        return val

    @property
    def splFail(self):
        val = self._wisTab.spellFailure(self.curWis)
        # Apply bonuses (race, other?)
        return val

    @property
    def baseCha(self):
        return self.savedata.cha
        #return self.baseAbilites[Abilities.chaStr]

    @baseCha.setter
    def baseCha(self, val):
        self.savedata.cha = val
        #self.baseAbilites[Abilities.chaStr] = val
        #self._guiObj.updateCharAbilities()

    @property
    def curCha(self):
        val = self.baseCha
        # Apply bonuses (race, other?)
        raceBonus = self._race.baseBonuses()
        if(Abilities.chaStr in raceBonus):
            val += raceBonus[Abilities.chaStr]
        return val

    @property
    def loyalAdj(self):
        val = self._chaTab.loyalAdj(self.curCha)
        # Apply bonuses (race, other?)
        return val

    @property
    def maxNoHM(self):
        val = self._chaTab.maxHM(self.curCha)
        # Apply bonuses (race, other?)
        return val

    @property
    def reacAdj(self):
        val = self._chaTab.reactAdj(self.curCha)
        # Apply bonuses (race, other?)
        return val

class SaveDataError(Exception):
    pass
    
class CharSaveData(object):
    char = 'Character'
    #Stored as children elements
    strName = 'Strength'
    intelName = 'Intelligence'
    dexName = 'Dexterity'
    wisName = 'Wisdom'
    conName = 'Constitution'
    chaName = 'Charisma'
    levelName = "Level" 
    
    #Stored as attributes
    nameAtt = "name"
    alignAtt = "alignment"
    charClassAtt = "class"
    raceAtt = "race"
    
    leveling = "Leveling"
    levelStats = "Level"
    curLevel = "lvl"
    hpAtt = "hpRoll"
    
    curInjury = "Injury"
    
    def __init__(self, fileName):
        if(not fileName):
            fileName = os.getcwd()
            fileName = fileName[0:fileName.rindex('\\')]
            fileName = fileName + '\saveData\charData.txt'
        
        try:
            self.file = open(fileName, 'r+')
            self.doc = parse(self.file)
            self.file.close()
        except xml.parsers.expat.ExpatError:
            self.createNewChar()
            self.save(fileName)
        except IOError:
            self.createNewChar()
            self.save(fileName)
        
        self.charElem = self.doc.getElementsByTagName(CharSaveData.char)[0]
        self.lvlElem = self.doc.getElementsByTagName(CharSaveData.leveling)[0]
    
    def save(self, fileName):
        saveFile = open(fileName, 'w+')
        output = self.doc.toprettyxml()
        print output
        saveFile.write(output)
           
    def createNewChar(self):
        self.doc = Document()
        self.saveData = self.doc.createElement('SaveData')
        self.charElem = self.doc.createElement(CharSaveData.char)
        self.lvlElem = self.doc.createElement(CharSaveData.leveling)
        self.inventElem = self.doc.createElement('Inventory')
        
        self.doc.appendChild(self.saveData)
        self.saveData.appendChild(self.charElem)
        self.saveData.appendChild(self.inventElem)
        self.saveData.appendChild(self.lvlElem)
        
        self.strength = 3
        self.intel = 3
        self.dex= 3
        self.wis = 3 
        self.con = 3
        self.cha = 3
        self.level = 1
        self.injury = 0

        self.name ="Name Me"
        self.charClass = Class.createClass(None)
        self.align = "Select Align"
        self.race = "Select Race"

    @property        
    def strength(self):
        return self.getCharChildElem(CharSaveData.strName)
        
    @strength.setter        
    def strength(self, val):
        self.setCharChildElem(CharSaveData.strName, val)

    @property        
    def intel(self):
        return self.getCharChildElem(CharSaveData.intelName)
        
    @intel.setter        
    def intel(self, val):
        self.setCharChildElem(CharSaveData.intelName, val)

    @property        
    def dex(self):
        return self.getCharChildElem(CharSaveData.dexName)
        
    @dex.setter        
    def dex(self, val):
        self.setCharChildElem(CharSaveData.dexName, val)

    @property        
    def wis(self):
        return self.getCharChildElem(CharSaveData.wisName)
        
    @wis.setter        
    def wis(self, val):
        self.setCharChildElem(CharSaveData.wisName, val)

    @property        
    def con(self):
        return self.getCharChildElem(CharSaveData.conName)
        
    @con.setter        
    def con(self, val):
        self.setCharChildElem(CharSaveData.conName, val)

    @property        
    def cha(self):
        return self.getCharChildElem(CharSaveData.chaName)

    @cha.setter        
    def cha(self, val):
        self.setCharChildElem(CharSaveData.chaName, val)

    @property        
    def level(self):
        return self.getCharChildElem(CharSaveData.levelName)

    @level.setter        
    def level(self, val):
        self.setCharChildElem(CharSaveData.levelName, val)
        
    def getCharChildElem(self, attName):
        elems = self.charElem.getElementsByTagName(attName)
        if len(elems) != 1:
            raise SaveDataError('1 {0} node expected. Found {1}'.format(attName, len(elems)))
        text = elems[0].firstChild
        return int(text.data)
    
    def setCharChildElem(self, attName, val):
        elems = self.charElem.getElementsByTagName(attName)
        if len(elems) > 1:
            raise SaveDataError('More than 1 {0} node'.format(attName))
        try:
            elem = elems[0]
            elem.removeChild(elem.firstChild)
        except IndexError:
            elem = self.doc.createElement(attName)
            self.charElem.appendChild(elem)
        textNode = self.doc.createTextNode(str(val))
        elem.appendChild(textNode)

    @property        
    def name(self):
        return self.charElem.getAttribute(CharSaveData.nameAtt)

    @name.setter        
    def name(self, val):
        self.charElem.setAttribute(CharSaveData.nameAtt, val)

    @property        
    def align(self):
        return self.charElem.getAttribute(CharSaveData.alignAtt)

    @align.setter        
    def align(self, val):
        self.charElem.setAttribute(CharSaveData.alignAtt, val)

    @property        
    def charClass(self):
        return self.charElem.getAttribute(CharSaveData.charClassAtt)

    @charClass.setter        
    def charClass(self, val):
        self.charElem.setAttribute(CharSaveData.charClassAtt, val.name)

    @property        
    def race(self):
        return self.charElem.getAttribute(CharSaveData.raceAtt)

    @race.setter        
    def race(self, val):
        self.charElem.setAttribute(CharSaveData.raceAtt, str(val))
        
    @property
    def lvlUps(self):
        elems = self.lvlElem.getElementsByTagName(CharSaveData.levelStats)
        rolls = []
        for x in elems:
            lvl = x.getAttribute(CharSaveData.curLevel)
            hp = x.getAttribute(CharSaveData.hpAtt)
            rolls.append((lvl, hp))
        rolls.sort()
        return [x[1] for x in rolls]
    
    @lvlUps.setter
    def lvlUps(self, val):
        elems = self.lvlElem.getElementsByTagName(CharSaveData.levelStats)
        for x in elems:
            self.lvlElem.removeChild(x)
        val.sort()
        for x in val:
            newElem = self.doc.createElement(CharSaveData.levelStats)
            newElem.setAttribute(CharSaveData.curLevel, str(x[0]))
            newElem.setAttribute(CharSaveData.hpAtt, str(x[1]))
            self.lvlElem.appendChild(newElem)
    
    @property
    def injury(self):
        return self.getCharChildElem(CharSaveData.curInjury)
    
    @injury.setter
    def injury(self, val):
        self.setCharChildElem(CharSaveData.curInjury, val)