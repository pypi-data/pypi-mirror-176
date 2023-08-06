'''Module to define the class of MB-30 Dassym's electronic board representation.

:author: F. Voillat
:date: 2021-02-24 Creation
'''


from .base import DBoard, DBoardPreferredDapiMode

class Board30(DBoard):
    '''Class for MB-30 Dassym's board.
    
    .. inheritance-diagram:: Board30
        :parts: 1
    
    '''
    
    number = '30'
    '''Board type number (str)'''
    
    def __init__(self, dapi, dmode=DBoardPreferredDapiMode.REGISTER):
        '''Constructor'''
        super().__init__(dapi, dmode)
        self.speed_range.set(1000,40000)
          
        
        
            