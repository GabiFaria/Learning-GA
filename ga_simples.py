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
				aux = aux + pop[i][j]*(2**k)
				k = k-1
			avaliacoes.append(aux**2)
			aux = 0
			k = tamanhogene-1
		return avaliacoes
	
	def Selecao (self,pop,avaliacao):
		probabilidade = []
		pais = []
		for i in range(len(avaliacao)):
			probabilidade.append((avaliacao[i]/sum(avaliacao))*100)
		pais.append(choices(pop,probabilidade,k=8))
		return pais			  
	
	def Crossover (self,pais,tamanhogene):
		point = random.randint(0,tamanhogene-2)
		filho2 = []
		fim = tamanhogene
		filho1 = []
		for i in range(len(pais[0])-1): 
			filho1.append(pais[0][i][:point]+pais[0][i+1][point:fim])
			filho2.append(pais[0][i+1][point:fim]+pais[0][i][0:point])
		
		return filho1+filho2
	

class Evolucao():
	
	def evoluindo(self,tamanhopop,tamanhogene):
		maximo = 0
		i = 0
		pop = []
		pais = []
		aval = []
		populacao = Mae_Natureza()
		pop=(populacao.InicializaPopulacao(tamanhopop,tamanhogene))
		while (maximo<3150):
			aval = (populacao.Avaliacao(pop,len(pop),tamanhogene))
			pais = (populacao.Selecao(pop,aval))
			pop.clear()
			pop =(populacao.Crossover(pais,tamanhogene))
			maximo = sum(aval)
			i+=1
			aval.clear()
			pais.clear()
		for i in range(len(pop)):
			print(pop[i])

e = Evolucao() 
tamanhopop = 10
tamanhogene = 4
e.evoluindo(tamanhopop,tamanhogene)
