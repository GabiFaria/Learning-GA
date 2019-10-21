
import random
import numpy as np
import NeuralNetwork.playground_Pong
from NeuralNetwork import Brain
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
        return (self.population)
            
    def Rating(self, Avaliador):
        avaliation = Avaliador(self.population,20).start()
        return avaliation
    
    def Selection(self,sizeselection,avaliation):
        probability = []
        parents = [] 
        if (sum(avaliation) == 0):
            parents.append(self.population)
            return (parents)   

        for i in range(len(avaliation)):
            probability.append((avaliation[i]/sum(avaliation))*100)
        parents.append(choices(self.population,probability, k=sizeselection))

        return parents

    def Crossover(self, parents, inputs, hidden, outputs):
        newchromossomes = []
        individualsgenes = []
        for k in range(len(parents[0])):
            individualsgenes.append(parents[0][k].GenesperPeso())
        fim = len(individualsgenes[0])
        point = random.randint(0,fim-2)
        son = []
        son1 = []
        temp = []
        for i in range(len(individualsgenes)-1):
            son.append(individualsgenes[i][:point]+individualsgenes[i+1][point:fim])
            son1.append(individualsgenes[i+1][point:fim]+individualsgenes[i][0:point])
        aux = son+son1
        for j in range(len(aux)):
            newchromossomes.append(Chromosome(inputs,hidden,outputs,ones = True))
            temp.append(newchromossomes[j].FromGeneperPesoCreatePesos(inputs,hidden,outputs,aux[j]))
            newchromossomes[j].pesos = temp[j]
        return newchromossomes
        
        
    #def Mutation(self, inputs, hidden, outputs):
     #   sizepop = len(self.population)
      #  sortitionchromossome = random.randint(0,sizepop-1)
       # sizegene = len(self.population[sortitionchromossome].pesos)
        #sortitiongene  = random.randint(0,sizegene-1)
        #genes = self.population[sortitionchromossome].GenesperPeso()
        #genes[sortitiongene] = (random.random()*2)-1
        #return ()
        #self.population[sortitionchromossome].pesos[sortitiongene]

    #def Competition():
    #    pass
        


def Evolution (generation, sizepop, sizeselection, inputs, hidden, outputs):
    generation.InitPopulation(sizepop,inputs, hidden, outputs)
    rating = generation.Rating(NeuralNetwork.playground_Pong.Avaliation)
    print (rating)
    while (True):
        parents = generation.Selection(sizeselection,rating,inputs,hidden,outputs)
        generation.population = generation.Crossover(parents, inputs, hidden, outputs)
        rating = generation.Rating(NeuralNetwork.playground_Pong.Avaliation)
        print (rating)
#        generation.Mutation(inputs,hidden,outputs)

if __name__ == "__main__":
    generation = MotherNature()
    Evolution(generation, 20,20, 2, [10,20,32], 1)