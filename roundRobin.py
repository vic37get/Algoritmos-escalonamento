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


def roundRobin(dados):
    #Retorno médio
    instanteTermino, instanteChegada = [], []
    #Resposta média
    chegadaProcesso, executadoProcesso = [], []
    #Espera Médio
    tempoEspera = 0
    instante = 0
    processos = TratamentoArquivo(dados)
    duracao_total = sum(processos['duracaoProcesso'])
    print(duracao_total)
    while instante < duracao_total:
        processos_candidatos = processos[(processos['instanteChegada'] <= instante) & (processos['status'] != 1)]
        print('Instante', instante)
        print('Processos:\n',processos)
        print('Processos candidatos:\n', processos_candidatos)
        if len(processos_candidatos) > 0:
            processo = processos_candidatos.iloc[0]
            print('Processo escolhido: \n', processos[processos['numProcesso'] == processo['numProcesso']])
            duracao = processo['duracaoProcesso']
            chegada = processo['instanteChegada']
            numProcesso = processo['numProcesso']
            executado = processo['executado']
            print('Duracao: ', duracao)

            if executado != 1:
                chegadaProcesso.append(chegada)
                executadoProcesso.append(instante)
                processos.loc[processos.numProcesso == numProcesso, 'executado'] = 1

            #Se a duração do processo ainda for maior ou igual a um quantum:
            if duracao - 2 >= 0:
                duracao-=2
                processos.loc[processos.numProcesso == numProcesso, 'duracaoProcesso'] = duracao
                print('Processo após executar:\n', processos[processos['numProcesso'] == processo['numProcesso']])
                print(processos)
                instante+=2
            #Se a duração for igual a 1:
            else:
                duracao-=1
                processos.loc[processos.numProcesso == numProcesso, 'duracaoProcesso'] = duracao
                print('Processo após executar:\n', processos[processos['numProcesso'] == processo['numProcesso']])
                print(processos)
                instante+=1
            tempoEspera+=((len(processos_candidatos) - 1))
            if duracao == 0:
                processos.loc[processos.numProcesso == numProcesso, 'status'] = 1
                instanteChegada.append(chegada)
                instanteTermino.append(instante)
        
        else:
            print(processos_candidatos)
            print('Processador ocioso')
            instante+=2

    print(instanteChegada, len(instanteChegada))
    print(instanteTermino, len(instanteTermino))
    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(tempoEspera, len(processos))

    return retorno_md, resposta_md, espera_md 

                
retornoMedio, respostaMedia, esperaMedia = roundRobin(dados)
print('RR %.2f %.2f %.2f' %(retornoMedio, respostaMedia, esperaMedia))
