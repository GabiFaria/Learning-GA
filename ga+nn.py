import random
import numpy as np
from NeuralNetwork.Playgraund.PlaygroundPong import Avaliation as Pong
from NeuralNetwork import Brain
from random import choices

class Chromosome (Brain):
    def __init__(self, inputs, hidden, output, ones=False):
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
    def __init__(self, avaliador, avaliatorIterations, sizepop = 0, inputs:int = 0, hidden:list = 0, output:int = 0, ones=False):
        self.population = []
        for i in range(sizepop):
            pop = Chromosome(inputs, hidden, output, ones=ones)
            self.population.append(pop)

        #Loop de evolução deve continuar?
        self.evolving = True
        #Avaliação da população atual
        self.rating = [0 for e in range(sizepop)]
        #Referencia da classe de avaliação
        self.avaliatorClass = avaliador
        #Objeto avaliador
        self.avaliator = avaliador(self.population, avaliatorIterations)
        #Quantidade de iterações da avaliação
        self.avaliatorIterations = avaliatorIterations

    def Rating(self):
        self.avaliator = self.avaliatorClass(self.population, self.avaliatorIterations)
        avaliation = self.avaliator.start()
        return avaliation
    
    def Selection(self, sizeselection, avaliation):
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
        


def Evolution (generation:MotherNature, sizeselection, inputs, hidden, outputs):
    #Salvando rating da geração atual 
    generation.rating = generation.Rating()
    while generation.evolving:
        parents = generation.Selection(sizeselection, generation.rating)
        generation.population = generation.Crossover(parents, inputs, hidden, outputs)
        generation.rating = generation.Rating()
        print(generation.rating)
        #generation.Mutation(inputs,hidden,outputs)

if __name__ == "__main__":
    #Cria o objeto Mae Natureza
    generation = MotherNature(Pong, 5, 20, 2, [20], 1)
    #Loop de evolução
    Evolution(generation, 10, 2, [20], 1)