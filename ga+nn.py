import random
import ANN.ANN
import numpy as np
from random import choices

class MotherNature ():
    def InitializeChromosome(self, inputs:int, hidden:list, output:int):
        genes = []
        chromosome = ANN.ANN.Brain(inputs,hidden,output,ones=False)
        for i in range((len(chromosome.pesos))):
            for j in range((len(chromosome.pesos[i]))):
                genes.append(chromosome.pesos[i][j])

        print (genes[0][0])      
        #print(chromosome.think(np.array([10, 20])))
        #print(chromosome.pesos)
        print (genes)
        return (chromosome)



    
a = MotherNature()
chromo = a.InitializeChromosome(2,[2],1)   
