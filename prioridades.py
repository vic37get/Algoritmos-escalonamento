import sys

import numpy as np
import pandas as pd

arquivo = sys.stdin
try:
    dados = arquivo.readlines()
except:
    print('Arquivo não encontrado!')
    exit(0)

def TratamentoArquivo(arquivo, prioridadeInicial):
    for linha in range(len(arquivo)):
        arquivo[linha] = arquivo[linha].replace('\n','').split()
        arquivo[linha].append(prioridadeInicial)
        arquivo[linha].append(0)
        arquivo[linha].append(0)
    dados = pd.DataFrame(arquivo, columns=['instanteChegada', 'duracaoProcesso', 'prioridade','executado', 'status'])
    dados = dados.astype(int)
    return dados

def MaiorPrioridade(dados):
    return max(dados['prioridade'])

def RetornoMedio(instanteChegada, instanteTermino):
    tempoRetorno = []
    for processo in range(len(instanteChegada)):
        tempo = instanteTermino[processo] - instanteChegada[processo]
        tempoRetorno.append(tempo)
    return sum(tempoRetorno)/len(tempoRetorno)

def RespostaMedia(chegadaProcesso, executadoProcesso):
    tempoResposta = []
    for processo in range(len(chegadaProcesso)):
        tempo = executadoProcesso[processo] - chegadaProcesso[processo]
        tempoResposta.append(tempo)
    return sum(tempoResposta)/len(tempoResposta)

def EsperaMedio(tempoEspera, processos):
    return tempoEspera/processos

def PrioridadesDinamicas(dados, prioridadeInicial):
    #Retorno médio
    instanteTermino, instanteChegada = [], []
    #Resposta média
    chegadaProcesso, executadoProcesso = [], []
    #Espera Médio
    tempoEspera = 0

    processos = TratamentoArquivo(dados, prioridadeInicial)
    duracao_total = sum(processos['duracaoProcesso'])
    instante = 0
    while(instante < duracao_total):
        escolhido = False
        processos_candidatos = processos[(processos['instanteChegada'] <= instante) & (processos['status'] != 1)]
        for processo in range(len(processos)):
            try:
                processos_candidatos.loc[processo]
                processoMaiorP = MaiorPrioridade(processos_candidatos)
                executado = processos['executado'][processo]
                chegada = processos['instanteChegada'][processo]
                duracao = processos['duracaoProcesso'][processo]
                prioridade = processos['prioridade'][processo]
                if (prioridade == processoMaiorP) and (duracao > 0) and (escolhido == False):

                    if executado != 1:
                        chegadaProcesso.append(chegada)
                        executadoProcesso.append(instante)
                        processos.loc[processo, 'executado'] = 1
                    
                    if (duracao - 1) > 0:
                        processos.loc[processo, 'prioridade'] = prioridade - 1

                    else:
                        processos.loc[processo, 'status'] = 1
                        instanteChegada.append(chegada)
                        instanteTermino.append((instante+1))
                    processos.loc[processo, 'duracaoProcesso'] = duracao - 1
                    escolhido = True

                else:
                    tempoEspera+=1
                    if duracao > 0 and chegada <= instante:
                        processos.loc[processo, 'prioridade'] = prioridade + 1
            except:
                continue
        instante+=1
    
    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(tempoEspera, len(processos))

    return retorno_md, resposta_md, espera_md 

retornoMedio, respostaMedia, esperaMedia = PrioridadesDinamicas(dados, 5)
print('PRI %.2f %.2f %.2f' %(retornoMedio, respostaMedia, esperaMedia))
