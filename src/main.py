from generate_inputs import generate_d_pa, generate_a_pr, generate_b_pe
from gurobi import gurobi

partidas = range(380)
rodadas = range(38)
arbitros = range(20)
equipes = range(20)

n_partidas = len(partidas)
n_rodadas = len(rodadas)
n_arbitros = len(arbitros)
n_equipes = len(equipes)

a_pr = generate_a_pr(n_partidas, n_rodadas)
d_pa = generate_d_pa(n_partidas, n_arbitros)
b_pe = generate_b_pe(n_partidas, n_equipes, n_rodadas)

gurobi(d_pa, a_pr, b_pe, arbitros, partidas, rodadas, equipes)