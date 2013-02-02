'''
Created on Jan 21, 2013

@author: Nabori
'''

class ItemException(Exception):
    pass

class Item(object):
    def __init__(self, name=None, weight=None, value=None):
        '''
        Constructor
        '''
        self.weight = weight
        self.value = value
        self.name = name
        
class Container(Item):
    def __init__(self, name=None, weight=None, value=None):
        '''
        Constructor
        '''
        super(Container, self).__init__(name, weight, value)
        
        self.zeroContentsWeight = False
        self.maxContentsWeight = None
        self.maxNoItems = None # Probably don't need
    