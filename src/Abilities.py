'''
Created on Jan 21, 2013

@author: Nabori
'''

import xlrd

dataDir = "..\data"

class AbilityTableException(Exception):
    pass

def value_from_key(sheet, colName, resColName, key):
    col_index = -1
    for index in xrange(sheet.ncols):
        if sheet.cell(0, index).value == colName:
            col_index = index
            break
    
    if(col_index < 0):
        raise AbilityTableException("Couldn't find key column")
    
    res_col_index = -1
    for index in xrange(sheet.ncols):
        if sheet.cell(0, index).value == resColName:
            res_col_index = index
            break

    if(res_col_index < 0):
        raise AbilityTableException("Couldn't find result column")

    for row_index in xrange(sheet.nrows):
        if sheet.cell(row_index, col_index).value == key:
            return sheet.cell(row_index, res_col_index).value
    
    print colName + str(col_index)    
    print resColName + str(res_col_index)
    print "Key:" + str(key)
    raise AbilityTableException("Couldn't find key in table")
    
class Abilities():
    strStr = "str"
    intStr = "int"
    conStr = "con"
    dexStr = "dex"
    wisStr = "wis"
    chaStr = "cha"
    
    fullList = [strStr, intStr, wisStr, dexStr, conStr, chaStr]
    
class AbilityTable(object):
    def __init__(self):
        '''
        Constructor
        '''
        self._workbook = None
        self._worksheet = None
        self.referenceBook = dataDir + r'\Reference.xlsx'

    @property
    def workbook(self):
        if(not self._workbook):
            self._workbook = xlrd.open_workbook(self.referenceBook)
        return self._workbook
    
    @property
    def worksheet(self):
        if(not self._worksheet):
            self._worksheet = self.workbook.sheet_by_name(self._sheetName)
        return self._worksheet

class StrTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Strength"
        super(StrTab, self).__init__()
    
    def unknownBonus(self, val):
        return "-" 

    def toHitBonus(self, val):
        return value_from_key(self.worksheet, "Score", "Hit", val)

    def dmgBonus(self, val):
        return value_from_key(self.worksheet, "Score", "Dmg", val)

    def weightAllow(self, val):
        return value_from_key(self.worksheet, "Score", "Wght", val)

    def maxPress(self, val):
        return value_from_key(self.worksheet, "Score", "Mx Press", val)

    def openDoors(self, val):
        return value_from_key(self.worksheet, "Score", "Doors", val)

    def bendBars(self, val):
        return value_from_key(self.worksheet, "Score", "Bend", val)

    #TODO: Encumberance
    
class ConTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Constitution"
        super(ConTab, self).__init__()
    
    def hpBonus(self, val):
        return value_from_key(self.worksheet, "Score", "HP", val) 

    def hpfBonus(self, val):
        return value_from_key(self.worksheet, "Score", "HPF", val)

    def shock(self, val):
        return value_from_key(self.worksheet, "Score", "Shock", val)

    def res(self, val):
        return value_from_key(self.worksheet, "Score", "Res", val)

    def NR(self, val):
        return value_from_key(self.worksheet, "Score", "NR", val)
    
class IntTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Intelligence"
        super(IntTab, self).__init__()
    
    def numLangs(self, val):
        return value_from_key(self.worksheet, "Score", "Lang", val) 

    def maxSpellLv(self, val):
        return value_from_key(self.worksheet, "Score", "Sp Lv", val)

    def knowSpell(self, val):
        return value_from_key(self.worksheet, "Score", "Know", val)

    def minKnownSpells(self, val):
        return value_from_key(self.worksheet, "Score", "Min S", val)

    def maxKnownSpells(self, val):
        return value_from_key(self.worksheet, "Score", "Max S", val)

    def illImmunity(self, val):
        return value_from_key(self.worksheet, "Score", "Illusion", val)

class WisTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Wisdom"
        super(WisTab, self).__init__()
    
    def magDefAdj(self, val):
        return value_from_key(self.worksheet, "Score", "Mag Def Adj", val) 

    def maxSpellLv(self, val):
        return value_from_key(self.worksheet, "Score", "Sp Lv", val)

    def bonusSpells(self, val):
        return value_from_key(self.worksheet, "Score", "Spl Merge", val)

    def spellFailure(self, val):
        return value_from_key(self.worksheet, "Score", "Spl Fail", val)

class DexTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Dexterity"
        super(DexTab, self).__init__()
    
    def reactAdj(self, val):
        return value_from_key(self.worksheet, "Score", "Adj Reaction", val) 

    def missleAdj(self, val):
        return value_from_key(self.worksheet, "Score", "Adj Missile", val)

#TODO: Determine these properties
    def dodgeAdj(self, val):
        return value_from_key(self.worksheet, "Score", "Adj Defense", val)

    def acAdj(self, val):
        return value_from_key(self.worksheet, "Score", "Adj Defense", val)

class ChaTab(AbilityTable):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._sheetName = "Charisma"
        super(ChaTab, self).__init__()
    
    def maxHM(self, val):
        return value_from_key(self.worksheet, "Score", "HM", val) 

    def loyalAdj(self, val):
        return value_from_key(self.worksheet, "Score", "LB", val)

    def reactAdj(self, val):
        return value_from_key(self.worksheet, "Score", "React", val)
