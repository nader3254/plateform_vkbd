# -*- coding: utf-8 -*-

class RF_BAND:
    def __init__(self):
        self.bandDict = {0: 'CHN:920~925MHz',
                         1: 'CHN2:840~845MHz',
                         2: 'CHN3:840~845MHz/920~925MHz',
                         3: 'FCC:902~928MHz',
                         4: 'ETSI:866~868MHz',
                         5: 'JPN:916.8~902.8MHz',
                         6: 'TWN:922.25~927.75MHz',
                         7: 'IDN:923.125~925.125MHz',
                         8: 'RUS:866.6~867.4MHz',
                         9: 'GBT:920~925MHz',
                         10: 'KOR:917.1~923.3MHz',
                         11: 'BRA:902~907MHz/915~928MHz',
                         12: 'MYS:919-923MHz',
                         13: 'OTHER:'}

    def getBandList(self):
        l = []
        for k, v in self.bandDict.items():
            l.append(v)
        return l
