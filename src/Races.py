'''
Created on Jan 21, 2013

@author: Nabori
'''
from Abilities import Abilities

class RaceException(Exception):
    pass

class Race(object):
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def baseBonuses(self):
        return {}
    
    @classmethod
    def createRace(cls, val):
        if(val.lower() == Dwarf.name):
            self = Dwarf()
        elif(val.lower() == Elf.name):
            self = Elf()
        elif(val.lower() == Gnome.name):
            self = Gnome()
        elif(val.lower() == HalfElf.name):
            self = HalfElf()
        elif(val.lower() == Halfling.name):
            self = Halfling()
        else:
            self= Human()
        return self
    
    def __str__(self):
        return self.name
    
class Human(Race):
    name = "human"
    def __init__(self):
        super(Human, self).__init__()

class Dwarf(Race):
    name = "dwarf"
    def __init__(self):
        super(Dwarf, self).__init__()

    def baseBonuses(self):
        return {
                    Abilities.conStr: 1,
                    Abilities.chaStr: -1
                }
    
class Elf(Race):
    name = "elf"
    def __init__(self):
        super(Elf, self).__init__()

    def baseBonuses(self):
        return {
                    Abilities.dexStr: 1,
                    Abilities.conStr: -1
                }

class Gnome(Race):
    name = "gnome"
    def __init__(self):
        super(Gnome, self).__init__()

    def baseBonuses(self):
        return {
                    Abilities.intStr: 1,
                    Abilities.wisStr: -1
                }

class HalfElf(Race):
    name = "half-elf"
    def __init__(self):
        super(HalfElf, self).__init__()

class Halfling(Race):
    name = "halfling"
    def __init__(self):
        super(Halfling, self).__init__()

    def baseBonuses(self):
        return {
                    Abilities.dexStr: 1,
                    Abilities.strStr: -1
                }

races = [Human.name, Elf.name, Dwarf.name, HalfElf.name, Halfling.name, Gnome.name]
