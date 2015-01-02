# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 18:46:07 2014

@author: Alex
"""

# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 


import numpy
import random
import matplotlib.pyplot as plt

#import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        
        
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb


    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.getClearProb
       
        
    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        
        a_prob=random.random()
        return a_prob<self.clearProb        

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum virus population for a patient. 
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        
        
        b_prob=random.random()
        
        if self.maxBirthProb * (1 - popDensity)>b_prob:
            return SimpleVirus(self.getMaxBirthProb, self.getClearProb)
            
        else: 
            raise NoChildException("No reproduction in this time step")



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses=viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)        


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update()
          
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        notCleared= []
        for virus in self.viruses:
            if not virus.doesClear():
                notCleared.append(virus)
        self.viruses =  notCleared[:]   #helper to avoid mutating object while iterating over its elements

        newViruses = []
        popDensity = self.getTotalPop()/float(self.getMaxPop)
        
        for vir in range(self.getTotalPop()):
            try:
                newViruses.append(self.viruses[vir].reproduce(popDensity))
            except NoChildException:
                pass
        self.viruses += newViruses
        return self.getTotalPop()


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    result_tot=numpy.zeros(300)
    
    res_avg=numpy.zeros(300)
    
    vir_init = [SimpleVirus(maxBirthProb, clearProb) for virus_id in range(numViruses)]  
    
    for i in range(numTrials): 
                   
        patient_one=Patient(vir_init, maxPop)
        for step in range(300):   # 300 = the NumSteps
            tot_pop_temp=patient_one.update()
            result_tot[step]+=tot_pop_temp
            
        res_avg=numpy.array(result_tot)/float(numTrials)
    plt.plot(res_avg, label="Total Virus Population")
    plt.title("Simple Virus simulation")
    plt.xlabel("Time")
    plt.ylabel("Average Virus Population")
    plt.legend(loc="best")



#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return  self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        return self.getResistances[drug]


    def reproduce(self, popDensity, activeDrugs):

        '''
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.        
        '''
        def resistsAll(activeDrugs):
            
            for drug in activeDrugs:
                if self.isResitantTo(drug)==True:
                    continue
                else:
                    break
            return True
        
        if resistsAll(activeDrugs)==True:
            b_prob=random.random()
            
#         For each drug resistance trait of the virus (i.e. each key of
#         self.resistances), the offspring has probability 1-mutProb of
#         inheriting that resistance trait from the parent, and probability
#         mutProb of switching that resistance trait in the offspring.       
        
            if self.maxBirthProb * (1 - popDensity)>b_prob:
                #resistances2={resistances for k in resistances}
            
                resistances2=self.getResistances[:]
                # resitances2={not resistances for k in resistances if not b_prob<1-mutProb}  ? ?
                for key in self.getResistances:
                    if not b_prob<1-self.mutProb:
                        resistances2[key]=not self.getResistances[key]
                        
                    
                return ResistantVirus(self.getMaxBirthProb, self.getClearProb, resistances2, self.getMutProb)
            
            else: 
                raise NoChildException
        
        
            

