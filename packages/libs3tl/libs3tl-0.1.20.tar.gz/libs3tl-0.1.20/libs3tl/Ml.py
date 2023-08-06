import os
from libs3tl import Step
import json
import pandas as pd
import pandas_datareader.data as web
import pickle
from datetime import date






class Ml(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ml"
        self.paramsFile = 'ML.properties'
        self.logger = 'logMl'
        self.logFile = self.getRelativeFile('../logs/Ml.log')

    def startup(self):
        super(Ml,self).startup()
        self.startSubscriber()

    def doWorkAndHandoff(self):
        pass

    def doWork(self):
        pass
        
    def computeML(self,msg):
        pass   
                
    def setpicklename(self,name):
        pass

    def getpicklename(self):
        pass
