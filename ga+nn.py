import random
from ANN.ANN import Brain
import numpy as np
from random import choices

class Chromosome (Brain):
    def __init__(self, inputs, hidden, output, ones=True):
        super().__init__(inputs, hidden, output, ones=ones)
        
    #Função que separa os genes por cada peso de um neurônio
    def GenesperPeso(self):
        genes = []
        aux = []
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                aux.append(self.pesos[i][j])

        for k in range(len(aux)):
            if (len(aux[k])>1):
                for l in range(len(aux[k])):
                    genes.append(aux[k][l]) 
            else:
                genes.append(aux[k][0])
        
        return (genes)

    #Função que monta a Rede Neural a partir dos genes
    def FromGeneperPesoCreatePesos(self, inputs, hidden, output,genes):
        aux = []
        peso=[]
        a = 0
        n = 0
        weight = []
        aux.append(inputs)
        for i in range(len(hidden)):
            aux.append(hidden[i])
        aux.append(output)

        for j in range(len(aux)):
            if (j<len(aux)-1):
                n = aux[j]*aux[j+1]
                peso.append(np.array(genes[a:a+n]))
                peso[j].shape=(aux[j],aux[j+1])
                a = a+n

        return peso

class MotherNature ():
    def InitPopulation(self,sizepop,inputs:int,hidden:list,output:int, ones=True):
        self.population = []
        for i in range(sizepop):
            pop=Chromosome(inputs,hidden,output,ones=False)
            self.population.append(pop)
            print(self.population[i].pesos)

    def Rating(self, Avaliador):
        avaliation = Avaliador.run(self.population,50)
        return avaliation
    
    def Selection(self,pop,avaliation):
        probability = []
        parents = [] 
        for i in range(len(avaliation)):
            probability.append((avaliation[i]/sum(avaliation))/100)
        parents.append(choices(pop,probability, k=8))
        return parents

    def Crossover(self, parents, sizegene):
        point = random.randint(0,sizegene-2)
        son = []
        son1 = []
        fim = sizegene
        parents.GenesperPeso();
        for i in range(len(parents[0]-1)):
            son.append(parents[0][i][:point]+parents[0][i+1][point:fim])
            son1.append(parents[0][i+1][point:fim]+parents[0][i][0:point])
        aux = son+son1
        for j in range(len(aux)):
            aux[j].FromGeneperPesoCreatePesos(aux[j].inputs,aux[j].hidden,aux[j].output,aux[j])
        return aux
        
        '''
    def Mutation():
        pass

    def Competition():
        pass
        
'''
a = MotherNature()
a.InitPopulation(2,2,[2,1],1,False)
