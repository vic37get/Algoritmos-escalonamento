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
        arquivo[linha].append(linha+1)
        arquivo[linha].append(0)
        arquivo[linha].append(0)
    dados = pd.DataFrame(arquivo, columns=['chegada', 'duracao', 'PID', 'posicao', 'executado', 'status'])
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
    duracao_total = sum(processos['duracao'])
    print(duracao_total)
    while instante < duracao_total:
        processos = processos.sort_values(by=['posicao'])
        processos_candidatos = processos[(processos['chegada'] <= instante) & (processos['status'] != 1)]
        print('Instante', instante)
        print('Processos:\n',processos)
        print('Processos candidatos:\n', processos_candidatos)
        
        if len(processos_candidatos) > 0:
            processo = processos_candidatos.iloc[0]
            print('Processo escolhido: \n', processos[processos['PID'] == processo['PID']])
            duracao = processo['duracao']
            chegada = processo['chegada']
            PID = processo['PID']
            executado = processo['executado']
            print('Duracao: ', duracao)
        

            if executado != 1:
                chegadaProcesso.append(chegada)
                executadoProcesso.append(instante)
                processos.loc[processos.PID == PID, 'executado'] = 1

            #Se a duração do processo ainda for maior ou igual a um quantum:
            if duracao - 2 >= 0:
                duracao-=2
                processos.loc[processos.PID == PID, 'duracao'] = duracao
                print('Processo após executar:\n', processos[processos['PID'] == processo['PID']])
                tempoEspera+=(((len(processos_candidatos))-1)*2)
                instante+=2
            #Se a duração for igual a 1:
            else:
                duracao-=1
                processos.loc[processos.PID == PID, 'duracao'] = duracao
                print('Processo após executar:\n', processos[processos['PID'] == processo['PID']])
                tempoEspera+=((len(processos_candidatos))-1)
                instante+=1
                

            if duracao == 0:
                processos.loc[processos.PID == PID, 'status'] = 1
                instanteChegada.append(chegada)
                instanteTermino.append(instante)
            
            else:
                ultimoDaFila = processos['posicao'].max()
                processos.loc[processos.PID == PID, 'posicao'] = ultimoDaFila + 1
        
        else:
            print(processos_candidatos)
            print('Processador ocioso')
            instante+=2
    
    print('Tempo de espera: ',tempoEspera)
    print(instanteChegada, len(instanteChegada))
    print(instanteTermino, len(instanteTermino))
    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(tempoEspera, len(processos))

    return retorno_md, resposta_md, espera_md 

retornoMedio, respostaMedia, esperaMedia = roundRobin(dados)
print('RR %.2f %.2f %.2f' %(retornoMedio, respostaMedia, esperaMedia))
