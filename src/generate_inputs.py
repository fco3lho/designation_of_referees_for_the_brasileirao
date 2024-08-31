import numpy as np
import random
from geopy.distance import geodesic

def generate_a_pr(p, r):
	matriz = np.zeros((p, r))

	for i in range(p):
		for j in range(r):
			if i >= ((j)*10) and i < (j+1)*10:
				matriz[i, j] = 1
			else:
				matriz[i, j] = 0

	return matriz

def generate_d_pa(p, a):
	matriz = np.zeros((p, a))

	capitais = {	
								"Belo Horizonte": (-19.927230, -43.945857), 
								"Curitiba": (-25.441091, -49.263032), 
								"Florianópolis": (-27.610763, -48.504662), 
								"Goiânia": (-16.696749, -49.267414), 
								"Porto Alegre": (-30.070150, -51.190201), 
								"Recife": (-8.053501, -34.904352), 
								"Rio de Janeiro": (-22.893805, -43.261288), 
								"Salvador": (-12.944368, -38.444124), 
								"São Paulo": (-23.562218, -46.636551)
							}
	cidades_jogos = list(capitais.keys())

	# Calcula a distância da cidade de cada jogo para cada árbitro,
	# usando de referência a variável 'capitais', com cada cidade
	# com sua respectiva coordenada geográfica
	for i in range(p): 
			cidade_jogo = cidades_jogos[i % len(cidades_jogos)] 
			for j in range(a):
					cidade_arbitro = cidades_jogos[j % len(cidades_jogos)]
					# print(f"Arbitro ({j}): {cidade_arbitro}")
					matriz[i, j] = geodesic(capitais[cidade_jogo], capitais[cidade_arbitro]).kilometers

	return matriz

def generate_b_pe(p, e, r):
	matriz = np.zeros((p, e))
	rodadas = [[] for _ in range(r)]

	# Lista de todos os possíveis confrontos (time1, time2)
	confrontos = [(i, j) for i in range(e) for j in range(i+1, e)]
	confrontos *= 2
	random.shuffle(confrontos)

	# Função para verificar se um time já jogou em uma rodada
	def time_ja_jogou_na_rodada(rodada, time):
			return any(time in jogo for jogo in rodada)

	# Distribuindo as partidas nas rodadas
	for confronto in confrontos:
			time1, time2 = confronto
			# Encontrar uma rodada onde ambos os times ainda não tenham jogado
			for rodada in rodadas:
					if not time_ja_jogou_na_rodada(rodada, time1) and not time_ja_jogou_na_rodada(rodada, time2):
							rodada.append(confronto)
							break

	# Preenchendo a matriz partidas x equipes com as partidas organizadas por rodada
	index = 0
	for rodada in rodadas:
			for jogo in rodada:
					time1, time2 = jogo
					matriz[index, time1] = 1
					matriz[index, time2] = 1
					index += 1

	# Se a matriz não foi completamente preenchida (index < partidas), adicionar confrontos faltantes
	faltam_partidas = p - index
	if faltam_partidas > 0:
			for i in range(faltam_partidas):
					time1, time2 = confrontos[index % len(confrontos)]
					matriz[index, time1] = 1
					matriz[index, time2] = 1
					index += 1

	return matriz