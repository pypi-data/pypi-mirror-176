# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 09:59:02 2022

@author: user
"""

import pickle as pkl
import numpy as np
import time
import os


this_dir, this_filename = os.path.split(__file__)  # Get path of data.pkl
data_path = os.path.join(this_dir, 'data.pkl')


def tanh(z):
    return (np.exp(z) - np.exp(-z))/(np.exp(z) + np.exp(-z))

def sigmoid(z):
    return 1/(1+np.exp(-z))




simulation = 0
try:
    import nidaqmx
    i=1
    c = True
    while c:
        try:
            entree = nidaqmx.Task()
            entree.ai_channels.add_ai_voltage_chan(f"Dev{i}/ai0")
            sortie = nidaqmx.Task()
            sortie.ao_channels.add_ao_voltage_chan(f"Dev{i}/ao0")
            c = False
        except:
            if(i<11):
                i=i+1
            else:
                c = False
                simulation = 1
except:
    simulation = 1


if(simulation):
    print("SIMULATION ACTIVÉE")
    
    # Load data
    file = open(data_path,"rb")
    X,weights = pkl.load(file)
    file.close()
    


class systeme_pression:
    
    
    def __init__(self):
        
        if(simulation):
            
            # Initialize simulation
            self.h = np.zeros([1,250])

            for i in range(len(X[0])):                
                self.h = X[0,i:i+1,:] @ weights[0] + self.h @ weights[1] + weights[2]
                self.h = tanh(self.h)
            
            # Initialize ouverture
            self.countA = 0
            self.maxA = np.random.randint(10,60)
            self.sortie = np.random.randint(0,101)/100
        
        else:
            
            self.sortie = None
        
    
    def prochaine_seconde( self,ouverture ):
        
        if(ouverture < 0):
            raise "Erreur de valeur d'ouverture"
        elif(ouverture > 100):
            raise "Erreur de valeur d'ouverture"
        
        ouverture = ouverture/100*5
        
        
        if(simulation == 0): # Real system
        
            sortie.write(ouverture)
            time.sleep(1) # Wait 1 second before measuring effect
            return 847.199 * entree.read()
        
        
        else: 
            time.sleep(1) # Simulate 1 second
            
            self.countA += 1
            if(self.countA >= self.maxA):
                self.countA = 0
                self.maxA = np.random.randint(10,60)
                self.sortie = np.random.randint(0,101)/100

            self.h = np.array([ [ ouverture , self.sortie ] ]) @ weights[0] + \
                self.h @ weights[1] + weights[2]
            self.h = tanh(self.h)
            
            p = self.h @ weights[3] + weights[4]
            p = sigmoid(p)
            
            p = p @ weights[5] + weights[6]
            p = p[0,0]
            
            p = p*847.199 # Analog read to PSI
            
            if(p < 0):
                p = 0
            elif(p > 36.5):
                p = 36.5
            
            return p
            
            
    def ouverture_sortie(self):
        
        return self.sortie*100




