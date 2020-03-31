# import statements
import os
import pandas as pd
import numpy as np
import datetime
import re

class BcaCalculator:
    
    def __init__(self, filename=None):
        """
        Initialize the class
        """
        self.filename = os.path.join('S:/Departments/Analytics/Chemical Analytics/Richard/tempUploadFolder', filename)
        self.sampleResults = pd.DataFrame(columns=['Dilution 1 (g/L)','Dilution 2 (g/L)','Mean Concentration (g/L)','Standard Deviations (%)','Variance (CV) (%)'])
        self.standardResults = pd.DataFrame(columns=['Mean Concentrations (g/L)','Variance (CV) (%)'])
        self.initialStandardsDataframe = pd.read_csv(self.filename, sep='\t', skiprows=2, nrows=14)
        self.initialUnknownsDataframe = pd.read_csv(self.filename, sep='\t', skiprows=24, skipfooter=11)
    
    def __repr__(self):
        return "Used to calculate results for BCA assays in place of previous copy/paste in excel method."
    
    def adjustConcentrations(self):
        # Used to adjust concentrations for golden toad, does nothing for non golden toad, but that is how it is labeled on the SoftMax template
        self.adjConcValues = [round(self.initialUnknownsDataframe.loc[index, 'AdjConc'],3) for index in range(0, len(self.initialUnknownsDataframe)) if index <= (len(self.initialUnknownsDataframe)-3) and index % 3 == 0]
        return self.adjConcValues
    
    def averageConcentrations(self):
        #Average the concentrations back calculated from different dilutions
        self.averageConcentrations_ = [round((self.adjConcValues[i]+self.adjConcValues[i+1])/2, 3) for i in range(len(self.adjustConcentrations())) if (i % 2) == 0]
        return self.averageConcentrations_
    
    def standardDeviations(self):
        #calculate standard deviations from sample values 
        self.standardDeviations_ = [round(np.std(self.adjConcValues[i:i+2]), 3) for i in range(len(self.adjustConcentrations())) if (i % 2) == 0]
        return self.standardDeviations_
    
    def coefficientsOfVariation(self):
        #calculate CV values
        self.coefficientsOfVariation_ = [round((self.standardDeviations()[i]/self.averageConcentrations()[i])*100, 3) for i in range(len(self.standardDeviations()))]
        return self.coefficientsOfVariation_
    
    def fillStandardsDataframe(self):
        for i in range(0, len(self.initialStandardsDataframe)):
            if i % 2 == 0:
                self.standardResults.loc[i, 'Variance (CV) (%)'] = self.initialStandardsDataframe.loc[i, 'CV']
        i = 0
        while i+2 <= len(self.initialStandardsDataframe):
            self.standardResults.loc[i, 'Mean Concentrations (g/L)'] = (self.initialStandardsDataframe.loc[i, 'BackCalcConc'] + self.initialStandardsDataframe.loc[i+1, 'BackCalcConc'])/2
            i += 2
        return self.standardResults
    
    def fillSamplesDataframe(self):
        for i in range(0, len(self.adjustConcentrations())):
            if i % 2 == 0:
                self.sampleResults.loc[i,'Dilution 1 (g/L)'] = self.adjConcValues[i]
            else:
                self.sampleResults.loc[i-1, 'Dilution 2 (g/L)'] = self.adjConcValues[i] 
        self.sampleResults['Mean Concentration (g/L)'] = self.averageConcentrations()
        self.sampleResults['Standard Deviations (%)'] = self.standardDeviations()
        self.sampleResults['Variance (CV) (%)'] = self.coefficientsOfVariation()
        self.sampleResults = self.sampleResults.rename(index = {0:0, 2:1, 4:2, 6:3, 8:4})
        return self.sampleResults

class GoldenToad(BcaCalculator):
    
    def adjustConcentrations(self):
        # Used to adjust concentrations for golden toad, does nothing for non golden toad, but that is how it is labeled on the SoftMax template
        self.adjConcValues = [round(self.initialUnknownsDataframe.loc[index, 'AdjConc']+self.initialUnknownsDataframe.loc[index + (0.5*len(self.initialUnknownsDataframe)), 'AdjConc'],3) for index in range(0, len(self.initialUnknownsDataframe)) if index <= (0.5*len(self.initialUnknownsDataframe)-3) and index % 3 == 0]
        return self.adjConcValues