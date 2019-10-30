import random
import numpy as np
from NeuralNetwork.Playgraund.PlaygroundPong import Avaliation as Pong
from NeuralNetwork import Brain
from random import choices

class Chromosome (Brain):
    def __init__(self, inputs, hidden, output, ones=False):
        super().__init__(inputs, hidden, output, ones=ones)
        #Número de entradas da RN
        self.inputs = inputs
        #Número de camadas escondidas da RN
        self.hidden = hidden
        #Número de saída da RN
        self.output = output
        #Se a RN é iniciada com 1's
        self.ones = ones
        
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

        self.generationCont = 0

        self.lastavaliation = 0

        self.lastpopulation = []

    def Rating(self):
        self.avaliator = self.avaliatorClass(self.population, self.avaliatorIterations)
        avaliation = self.avaliator.start()
        return avaliation
    
    def Selection(self, sizeselection, avaliation):
        probability = []
        parents = []
        if (sum(avaliation) == 0):
            a = MotherNature(self.avaliatorClass,self.avaliatorIterations, sizeselection, self.population[0].inputs, self.population[0].hidden, self.population[0].output, False)
            parents.append(a.population)
            random.shuffle(parents)
            return (parents)   
        else:
            for i in range(len(avaliation)):
                probability.append((avaliation[i]/sum(avaliation))*100)
            parents.append(choices(self.population,probability, k=sizeselection))
            random.shuffle(parents)
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
          
    def Mutation(self, avaliation, chromossomeprobability, geneprobability):
        individualgenes = []
        temppesos = []
        newchromossome = []
        for k in range(len(self.population)):
            individualgenes.append(self.population[k].GenesperPeso())
        for i in range(len(self.population)):
            mut = random.random()
            if (mut<=chromossomeprobability):
                for j in range(len(individualgenes[i])):
                    mut1 = random.random()
                    if (mut1<=geneprobability):
                        individualgenes[i][j] = (random.random()*2)-1
            temppesos.append(self.population[i].FromGeneperPesoCreatePesos(self.population[i].inputs,self.population[i].hidden,self.population[i].output,individualgenes[i]))
            self.population[i].pesos = temppesos[i]
    '''
    def Tournament (self):
        for i in range(len(self.lastavaliation)):
            if (self.lastavaliation[i]>self.rating[i]):
                self.population[i]= self.lastpopulation[i]
        for j in range(len(self.population)):
            print(self.population[j].pesos)
            print("\n")
'''
      
def Evolution (generation:MotherNature, sizeselection, inputs, hidden, outputs,callback=None):
    #Salvando rating da geração atual 
    generation.rating = generation.Rating()
    #print("primeira geracao")
    #print(generation.rating)
    while generation.evolving:
        parents = generation.Selection(sizeselection, generation.rating)
        generation.lastpopulation = generation.population
        generation.population = generation.Crossover(parents, inputs, hidden, outputs)
        generation.lastavaliation = generation.rating
        generation.rating = generation.Rating()
        #print("avaliacao da nova pop")
        #print(generation.rating)
        #generation.population = generation.Tournament()
        #print("avaliacao após tournament")
        #generation.rating = generation.Rating()
        if (callback!=None):
            callback()
        generation.generationCont +=1
        if (sum(generation.lastavaliation)>sum(generation.rating)): 
            generation.Mutation(generation.rating,0.03,0.10)

if __name__ == "__main__":
    #Cria o objeto Mae Natureza
    generation = MotherNature(Pong, 10, 20, 2, [20], 1)
    #Loop de evolução
    Evolution(generation, 11, 2, [20], 1, lambda:print(generation.rating))