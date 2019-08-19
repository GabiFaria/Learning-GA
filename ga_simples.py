import random
from random import choices

def InicializaCromossomo (tamanhogene):
	i = 0
	genes = []
	for i in range(tamanhogene):
		if (random.random()<0.5):
			genes.append(0)
		else:
			genes.append(1)
	return (genes)
def InicializaPopulacao (tamanhopop,tamanhogene):
	i = 0 
	cromossomos =  []
	for i in range(tamanhopop):
		cromossomos.append(InicializaCromossomo(tamanhogene))

	return cromossomos

def Avaliacao (populacao,tamanhopop,tamanhogene):
	avaliacoes = []
	aux =0 
	k= tamanhogene-1
	for i in range(tamanhopop):
		for j in range(tamanhogene):
			aux = aux + populacao[i][j]*(2**k)
			k = k-1
		avaliacoes.append(aux**2)
		aux = 0
		k = tamanhogene-1
	return avaliacoes

def Selecao (populacao, avaliacao):
	probabilidade = []
	pais = []
	for i in range(len(avaliacao)):
		probabilidade.append((avaliacao[i]/sum(avaliacao))*100)
	pais.append(choices(populacao,probabilidade,k=6))
	return pais			  

def Crossover (pais,tamanhogene):
	point = random.randint(0,tamanhogene-2)
	filho1 = []
	filho2 = []
	fim = tamanhogene
	
	for i in range(len(pais[0])-1): 
		filho1.append(pais[0][i][0:point]+pais[0][i+1][point:fim])
		filho2.append(pais[0][i+1][point:fim]+pais[0][i][0:point])
	return filho1+filho2


	
populacao= InicializaPopulacao(10,4)
avaliacoes = Avaliacao(populacao,10,4)
print (Avaliacao(populacao,10,4))
for i in range (4): 
	pais = Selecao(populacao,avaliacoes)
	newpopulacao = Crossover(pais,4)
	print (Avaliacao(newpopulacao,10,4))
	

