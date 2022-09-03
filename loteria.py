import random
import sys

import numpy as np
import pandas as pd

arquivo = sys.stdin
try:
    dados = arquivo.readlines()
except:
    print('Arquivo não encontrado!')
    exit(0)

def TratamentoArquivo(arquivo):
    for linha in range(len(arquivo)):
        arquivo[linha] = arquivo[linha].replace('\n','').split()
        arquivo[linha].append(linha)
        arquivo[linha].append(0)
        arquivo[linha].append(0)
    dados = pd.DataFrame(arquivo, columns=['instanteChegada', 'duracaoProcesso', 'numProcesso','executado', 'status'])
    dados = dados.astype(int)
    return dados

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

def Loteria(dados):
    #Retorno médio
    instanteTermino, instanteChegada = [], []
    #Resposta média
    chegadaProcesso, executadoProcesso = [], []
    #Espera Médio
    tempoEspera = 0

    processos = TratamentoArquivo(dados)
    duracao_total = sum(processos['duracaoProcesso'])
    instante = 0
    while(instante < duracao_total):
        processos_candidatos = processos[(processos['instanteChegada'] <= instante) & (processos['status'] != 1)]
        processo = random.choice(processos_candidatos['numProcesso'].values.tolist())
        #print('escolhido:', processo)
        #print(processos_candidatos)
        status = processos['status'][processo]
        executado = processos['executado'][processo]
        chegada = processos['instanteChegada'][processo]
        duracao = processos['duracaoProcesso'][processo]
        num_processo = processos['numProcesso'][processo]

        if executado != 1:
            chegadaProcesso.append(chegada)
            executadoProcesso.append(instante)
            processos.loc[processo, 'executado'] = 1

        processos.loc[processo, 'duracaoProcesso'] = duracao - 1
        if processos['duracaoProcesso'][processo] == 0:
            processos.loc[processo, 'status'] = 1
            instanteChegada.append(chegada)
            instanteTermino.append((instante+1))
        
        instante+=1
        tempoEspera+=((len(processos_candidatos) - 1))

    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(tempoEspera, len(processos))

    return retorno_md, resposta_md, espera_md 
        
retornoMedio, respostaMedia, esperaMedia = Loteria(dados)
print('LOT %.2f %.2f %.2f' %(retornoMedio, respostaMedia, esperaMedia))
