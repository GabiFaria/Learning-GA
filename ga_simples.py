import random
from random import choices

class Mae_Natureza:
	
	def InicializaCromossomo (self,tamanhogene):
		i = 0
		genes = []
		for i in range(tamanhogene):
			if (random.random()<0.7):
				genes.append(0)
			else:
				genes.append(1)
		return (genes)
	
	def InicializaPopulacao (self,tamanhopop,tamanhogene):
		i = 0 
		cromossomos =  Mae_Natureza()
		cromo = []
		for i in range(tamanhopop):
			cromo.append(cromossomos.InicializaCromossomo(tamanhogene))

		return cromo
	
	def Avaliacao (self,pop,tamanhopop,tamanhogene):
		avaliacoes = []
		aux =0 
		k= tamanhogene-1
		for i in range(tamanhopop):
			for j in range(tamanhogene):
				aux = aux + pop[0][i][j]*(2**k)
				k = k-1
			avaliacoes.append(aux**2)
			aux = 0
			k = tamanhogene-1
		return avaliacoes
	
	def Selecao (self,pop,avaliacao):
	
		probabilidade = []
		pais = []
		for i in range(len(avaliacao)):
			probabilidade.append((avaliacao[0][i]/sum(avaliacao[0]))*100)
		pais.append(choices(pop,probabilidade,k=6))
		return pais			  
	
	def Crossover (self,pais,tamanhogene):
		point = random.randint(0,tamanhogene-2)
		filho1 = []
		filho2 = []
		fim = tamanhogene
		
		for i in range(len(pais[0])-1): 
			filho1.append(pais[0][i][0:point]+pais[0][i+1][point:fim])
			filho2.append(pais[0][i+1][point:fim]+pais[0][i][0:point])
		return filho1+filho2


class Evolucao():
	
	def evoluindo(self,tamanhopop,tamanhogene):
		maximo = 0
		i = 0
		while (maximo<2550):
			populacao = Mae_Natureza()
			pais = []
			pop = []
			aval = []
			pop.append(populacao.InicializaPopulacao(tamanhopop,tamanhogene))
			aval.append(populacao.Avaliacao(pop,tamanhopop,tamanhogene))
			pais.append(populacao.Selecao(pop,aval))
			pop.clear()
			pop.append(populacao.Crossover(pais,tamanhogene))
			maximo = sum(aval[0])
			i+=1
			print ("Somátorio das avaliacões da ",i,"º População:",maximo)

e = Evolucao() 
tamanhopop = 10
tamanhogene = 4
e.evoluindo(tamanhopop,tamanhogene)
