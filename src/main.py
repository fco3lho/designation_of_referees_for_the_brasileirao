from generate_inputs import generate_d_pa, generate_a_pr, generate_b_pe
from gurobi import gurobi

capitais_distantes = {	
							"Belém": (-1.378558, -48.474792),
							"Manaus": (-3.039516, -60.050535),
							"São Luís": (-2.587037, -44.238891),
							"Fortaleza": (-3.778141, -38.535419),
							"Palmas": (-10.296865, -48.350315),
							"Natal": (-5.773912, -35.361941),
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

capitais_proximas = {	
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

# Número de partidas = 380
partidas = range(380)
# Número de rodadas = 38
rodadas = range(38)
# Número de árbitros = 20
arbitros = range(20)
# Número de equipes = 20
equipes = range(20)

n_partidas = len(partidas)
n_rodadas = len(rodadas)
n_arbitros = len(arbitros)
n_equipes = len(equipes)

# Distância entre o local da Partida p para o local de origem do Árbitro a.
a_pr = generate_a_pr(n_partidas, n_rodadas)

# 1 se a Partida p pertence a Rodada r, 0 caso contrário
d_pa = generate_d_pa(n_partidas, n_arbitros, capitais_proximas, capitais_distantes)

# 1 se a Partida p contém a Equipe e, 0 caso contrário
b_pe = generate_b_pe(n_partidas, n_equipes, n_rodadas)

# Tenta achar a solução ótima
gurobi(d_pa, a_pr, b_pe, arbitros, partidas, rodadas, equipes)