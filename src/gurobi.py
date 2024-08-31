import gurobipy as gp
from gurobipy import GRB

def gurobi(d_pa, a_pr, b_pe, A, P, R, E):
  # Criar o modelo
  model = gp.Model()
  model.setParam(GRB.Param.LogToConsole, 0)

  # Criação das variáveis de decisão
  x_pa = model.addVars(P, A, vtype=GRB.BINARY, name="x_pa")

  # Função objetivo: minimizar a soma das distâncias
  model.setObjective(gp.quicksum(x_pa[p, a] * d_pa[p, a] for p in P for a in A), GRB.MINIMIZE)

  ############## Restrições

  # Exatamente 1 árbitro deve ser designado para cada partida
  for p in P:
      model.addConstr(gp.quicksum(x_pa[p, a] for a in A) == 1, name=f"r1_p{p}")

  # Cada árbitro pode apitar no máximo 1 jogo por rodada
  for a in A:
      for r in R:
          model.addConstr(gp.quicksum(a_pr[p, r] * x_pa[p, a] for p in P) <= 1, name=f"r2_a{a}_r{r}")

  # Número total de partidas apitadas por cada árbitro deve estar no intervalo permitido, entre 18 e 20
  for a in A:
      model.addConstr(gp.quicksum(x_pa[p, a] for p in P) >= 18, name=f"r3_min_a{a}")
      model.addConstr(gp.quicksum(x_pa[p, a] for p in P) <= 20, name=f"r3_max_a{a}")

  # Limite de jogos de uma mesma equipe pelo mesmo árbitro
  for a in A:
      for e in E:
          model.addConstr(gp.quicksum(b_pe[p, e] * x_pa[p, a] for p in P) <= 2, name=f"r4_max_a{a}_e{e}")
          model.addConstr(gp.quicksum(b_pe[p, e] * x_pa[p, a] for p in P) >= 1, name=f"r4_min_a{a}_e{e}")

  ##############

  # Otimização
  model.optimize()

  # Exibir os resultados
  if model.status == GRB.OPTIMAL:
      print("Solução ótima encontrada:")
      for p in P:
          for a in A:
              if x_pa[p, a].x == 1:
                  print(f"Partida {p+1} será apitada pelo árbitro {a+1}.")
  else:
      print("Não foi encontrada uma solução ótima.")