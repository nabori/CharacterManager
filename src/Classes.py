'''
Created on Feb 2, 2013

@author: Nabori
'''
import xlrd

dataDir = "..\data"

class ClassException(Exception):
    pass

def value_from_key(sheet, colName, resColName, key):
    col_index = -1
    for index in xrange(sheet.ncols):
        if sheet.cell(0, index).value == colName:
            col_index = index
            break
    
    if(col_index < 0):
        raise ClassException("Couldn't find key column")
    
    res_col_index = -1
    for index in xrange(sheet.ncols):
        if sheet.cell(0, index).value == resColName:
            res_col_index = index
            break

    if(res_col_index < 0):
        raise ClassException("Couldn't find result column")

    for row_index in xrange(sheet.nrows):
        if sheet.cell(row_index, col_index).value == key:
            return sheet.cell(row_index, res_col_index).value
    
    print colName + str(col_index)    
    print resColName + str(res_col_index)
    print "Key:" + str(key)
    raise ClassException("Couldn't find key in table")

def get_vals_from_column(sheet, colName):
    col_index = -1
    for index in xrange(sheet.ncols):
        if sheet.cell(0, index).value == colName:
            col_index = index
            break
    
    if(col_index < 0):
        raise ClassException("Couldn't find key column")
    
    return [sheet.cell(row_index, col_index).value for row_index in xrange(1, sheet.nrows)]

class Class(object):
    name = "Select Class"
    def __init__(self):
        '''
        Constructor
        '''
        self._workbook = None
        self._worksheet = None
        self.referenceBook = dataDir + r'\Reference.xlsx'

    
    @classmethod
    def createClass(cls, val):
        if(val is None):
            self = Class()
        elif(val.lower() == Fighter.name):
            self = Fighter()
        elif(val.lower() == Mage.name):
            self = Mage()
        elif(val.lower() == Thief.name):
            self = Thief()
        elif(val.lower() == Cleric.name):
            self = Cleric()
        else:
            raise ClassException("Invalid class specified")
        return self
    
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

    @property
    def possibleLevels(self):
        return get_vals_from_column(self.worksheet, "Levels")
    
    @property
    def hpBonusPerLvl(self):
        return 0
        
class Fighter(Class):
    name = "fighter"
    def __init__(self):
        super(Fighter, self).__init__()
        self._sheetName = "Fighter"
    
    def xpForLvl(self, lvl):
        return int(value_from_key(self.worksheet, "Levels", "Next Lv XP", lvl))
    
    @property
    def hpBonusPerLvl(self):
        return 2
    
class Mage(Class):
    name = "mage"
    def __init__(self):
        super(Mage, self).__init__()
        self._sheetName = "Mage"

class Thief(Class):
    name = "thief"
    def __init__(self):
        super(Thief, self).__init__()
        self._sheetName = "Thief"

class Cleric(Class):
    name = "cleric"
    def __init__(self):
        super(Cleric, self).__init__()
        self._sheetName = "Cleric"

classes = [Class.name, Fighter.name, Mage.name, Thief.name, Cleric.name]
