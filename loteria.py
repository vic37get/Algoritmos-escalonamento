import copy
import random

import pandas as pd


def TratamentoArquivo(arquivo):
    dados = copy.deepcopy(arquivo)
    for linha in range(len(dados)):
        dados[linha] = dados[linha].replace('\n','').split()
        dados[linha].append(linha)
        dados[linha].append(0)
        dados[linha].append(0)
    df = pd.DataFrame(dados, columns=['instanteChegada', 'duracaoProcesso', 'numProcesso','executado', 'status'])
    df = df.astype(int)
    return df

#Termino do processo - Chegada do processo
def RetornoMedio(instanteChegada, instanteTermino):
    tempoRetorno = []
    for processo in range(len(instanteChegada)):
        tempo = instanteTermino[processo] - instanteChegada[processo]
        tempoRetorno.append(tempo)
    return sum(tempoRetorno)/len(tempoRetorno)

#Execução do processo - Chegada do processo
def RespostaMedia(chegadaProcesso, executadoProcesso):
    tempoResposta = []
    for processo in range(len(chegadaProcesso)):
        tempo = executadoProcesso[processo] - chegadaProcesso[processo]
        tempoResposta.append(tempo)
    return sum(tempoResposta)/len(tempoResposta)

#Soma dos períodos em que o processo estava no estado pronto.
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
        print('Processos candidatos:\n', processos_candidatos)
        if len(processos_candidatos) > 0:
            processo = random.choice(processos_candidatos['numProcesso'].values.tolist())
            print('Processo escolhido:\n', processo)
            executado = processos['executado'][processo]
            chegada = processos['instanteChegada'][processo]
            duracao = processos['duracaoProcesso'][processo]

            if executado != 1:
                chegadaProcesso.append(chegada)
                executadoProcesso.append(instante)
                processos.loc[processo, 'executado'] = 1

            processos.loc[processo, 'duracaoProcesso'] = duracao - 1
            print('Processo após executar:\n', processos.iloc[processo])
            if processos['duracaoProcesso'][processo] == 0:
                processos.loc[processo, 'status'] = 1
                instanteChegada.append(chegada)
                instanteTermino.append((instante+1))
            
            instante+=1
            tempoEspera+=((len(processos_candidatos) - 1))
        else:
            print('Processador ocioso')
            instante+=1

    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(tempoEspera, len(processos))

    return retorno_md, resposta_md, espera_md 
