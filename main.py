from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

equipe = {
  "Campos FC": {"cidade": "Campos", "torcedores": 23},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
  "SE Leões": {"cidade": "Leão", "torcedores": 40},
   "Simba FC": {"cidade": "Leão", "torcedores": 15},
  "SE Granada": {"cidade": "Granada", "torcedores": 10}
}

RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)
# Jogos (timex X timey) que ja foram atribuidos à uma rodada
JOGADOS = []

# gera combinação de todos os jogos

combinacao_de_todos_jogos = []
for e1 in equipe.keys():
  for e2 in equipe.keys():
    # # remove jogos com o mesmo time
    if e1 != e2:
      combinacao_de_todos_jogos.append((e1, e2))

# Dica 1: Fazer Restrições Genéricas
class UmTimePorRodadaRestricao(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  # atribuicao = {"variavel1": "valor1", "variavel2": "valor2", ...}
  def esta_satisfeita(self, atribuicao):
    rodadas = {}
    for i in range(RODADAS): # rodadas
      rodadas["R" + str(i)] = []

    # Sempre verifica TODOS os jogos. Exemplo: Caso o backtracking esteja vendo o R0J1, aqui
    # SEMPRE estara vendo o R0J0
    for variavel in atribuicao.keys():
      rodada = variavel[0:2]
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
        if (time1 in rodadas[rodada] or time2 in rodadas[rodada] and time2):
          return False
        else:
          rodadas[rodada].append(time1)
          rodadas[rodada].append(time2)
          JOGADOS.append(times)
    return True

if __name__ == "__main__":
    variaveis = []
    for i in range(RODADAS): # rodadas
      for j in range(JOGOS): # jogos
        # Variável RnJm, tal que n é o número da rodada e m é o jogo da rodada
        variaveis.append("R" + str(i) + "J" + str(j))
      
    dominios = {}
    for variavel in variaveis:
        # o domínio são as combinações de todos os possívels jogos
        dominios[variavel] = combinacao_de_todos_jogos
    
    problema = SatisfacaoRestricoes(variaveis, dominios)
    problema.adicionar_restricao( UmTimePorRodadaRestricao(variaveis) )
    
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      print("cabou")
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\tCidade: " + equipe[jogo[0]]["cidade"])