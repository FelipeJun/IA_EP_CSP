from satisfacao_restricoes import Restricao, SatisfacaoRestricoes

equipe = {
  # "Campos FC": {"cidade": "Campos", "torcedores": 23},
  "Guardiões FC": {"cidade": "Guardião", "torcedores": 40},
  "SE Leões": {"cidade": "Leão", "torcedores": 40},
  "CA Protetores": {"cidade": "Guardião", "torcedores": 20},
  "Simba FC": {"cidade": "Leão", "torcedores": 15},
  # "SE Granada": {"cidade": "Granada", "torcedores": 10},
  "Porto EC": {"cidade": "Porto", "torcedores": 45},
  "SE Escondidos": {"cidade": "Escondidos", "torcedores": 50}
}

RODADAS = (len(equipe)-1) * 2
JOGOS = int(len(equipe)/2)

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
    rodada = list(atribuicao.keys())[-1]
    rodada = rodada[0:2]
    jogosRodada = [x for x in list(atribuicao.keys()) if x.__contains__(rodada)]
    rodadas = []

    for variavel in jogosRodada:
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
        if (time1 in rodadas or time2 in rodadas):
          return False
        else:
          rodadas.append(time1)
          rodadas.append(time2)
    return True

class UmEstadioPorRodada(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)

  def esta_satisfeita(self, atribuicao):
    cidades_rodadas = []
    rodada = list(atribuicao.keys())[-1]
    rodada = rodada[0:2]
    jogosRodada = [x for x in list(atribuicao.keys()) if x.__contains__(rodada)]

    for variavel in jogosRodada:
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]

        if(len(cidades_rodadas) % JOGOS == 0):
          cidades_rodadas = []

        if (equipe[time1]["cidade"] in cidades_rodadas):
          return False
        else:
          cidades_rodadas.append(equipe[time1]["cidade"])
    return True

class UmClassicoPorRodada(Restricao):
  def __init__(self,variaveis):
    super().__init__(variaveis)
  def esta_satisfeita(self, atribuicao):
    rodada = list(atribuicao.keys())[-1]
    rodada = rodada[0:2]
    jogosRodada = [x for x in list(atribuicao.keys()) if x.__contains__(rodada)]
    eClassico = 0
    
    for variavel in jogosRodada:
      times = atribuicao[variavel]
      if times is not None:
        time1 = times[0]
        time2 = times[1]
      if (equipe[time1]["torcedores"] >= 38 and equipe[time2]["torcedores"] >= 38):
        eClassico += 1
    if eClassico >= 2:
      return False
    else:
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
    problema.adicionar_restricao(UmTimePorRodadaRestricao(variaveis))
    problema.adicionar_restricao(UmEstadioPorRodada(variaveis))
    problema.adicionar_restricao(UmClassicoPorRodada(variaveis))
    resposta = problema.busca_backtracking()
    if resposta is None:
      print("Nenhuma resposta encontrada")
    else:
      print("cabou")
      for i in range(RODADAS): # rodadas
        print("\n---------- Rodada " + str(i+1) + " ----------\n")
        for j in range(JOGOS): # jogos
          jogo = resposta["R" + str(i) + "J" + str(j)]
          print("Jogo " + str(j+1) + ": " + jogo[0] + " x " + jogo[1] + "\nCidade: " + equipe[jogo[0]]["cidade"] + "\n")