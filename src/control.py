'''
Created on Jan 21, 2013

@author: Nabori
'''

from Character import Character

class ViewControl(object):
    baseStr
    def __init__(self):
        self.char = Character(self)

    
if __name__ == '__main__':

    import sys
    
    
    app = QtGui.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
#    gui2 = MainWindow()
#    gui2.show()
    sys.exit(app.exec_())
