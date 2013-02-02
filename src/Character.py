'''
Created on Jan 21, 2013

@author: Nabori
'''

from Abilities import StrTab, IntTab, ConTab, DexTab, WisTab, ChaTab, Abilities
from Races import Race, Human
from Classes import Class

import itertools
class RefLists():
    order = ["Lawful", "Neutral", "Chaotic"]
    morality = ["Good", "Neutral", "Evil"]
    aligns = map("-".join, itertools.product(order, morality))
    
class Character(object):
    '''
    
    '''

    def __init__(self, guiObj):
        '''
        '''
        self.baseAbilites = {}
        for x in Abilities.fullList:
            self.baseAbilites[x] = 3
        
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
        print "Character.save() called"

    def load(self, fileName):
        print "Character.load() called"

    @property
    def race(self):
        return self._race
            
    @property
    def cls(self):
        return self._class

    @race.setter
    def race(self, val):
        self._race = Race.createRace(val)
        self._guiObj.updateCharAbilities()
        
    @property
    def baseStr(self):
        return self.baseAbilites[Abilities.strStr]

    @baseStr.setter
    def baseStr(self, val):
        self.baseAbilites[Abilities.strStr] = val
        self._guiObj.updateCharAbilities()

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
        return self.baseAbilites[Abilities.intStr]

    @baseInt.setter
    def baseInt(self, val):
        self.baseAbilites[Abilities.intStr] = val
        self._guiObj.updateCharAbilities()

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
        return self.baseAbilites[Abilities.conStr]

    @baseCon.setter
    def baseCon(self, val):
        self.baseAbilites[Abilities.conStr] = val
        self._guiObj.updateCharAbilities()

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
        return self.baseAbilites[Abilities.dexStr]

    @baseDex.setter
    def baseDex(self, val):
        self.baseAbilites[Abilities.dexStr] = val
        self._guiObj.updateCharAbilities()

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
        return self.baseAbilites[Abilities.wisStr]

    @baseWis.setter
    def baseWis(self, val):
        self.baseAbilites[Abilities.wisStr] = val
        self._guiObj.updateCharAbilities()

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
        return self.baseAbilites[Abilities.chaStr]

    @baseCha.setter
    def baseCha(self, val):
        self.baseAbilites[Abilities.chaStr] = val
        self._guiObj.updateCharAbilities()

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
