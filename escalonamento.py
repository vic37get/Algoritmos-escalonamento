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
    dados = pd.DataFrame(arquivo, columns=['instanteChegada', 'duracaoProcesso', 'prioridade'])
    dados = dados.astype(int)
    return dados

def MaiorPrioridade(dados):
    return max(dados['prioridade'])

def PrioridadesDinamicas(dados, prioridadeInicial):
    processos = TratamentoArquivo(dados, prioridadeInicial)
    duracao_total = sum(processos['duracaoProcesso'])
    instante = 0
    while(instante < duracao_total):
        #print(processos)
        escolhido = False
        processos_candidatos = processos[processos['instanteChegada'] <= instante]
        for processo in range(len(processos)):
            print(processos.iloc[[processo]])
            if processos.iloc[[processo]] in processos_candidatos:
                print(processo)
                processoMaiorP = MaiorPrioridade(processos_candidatos)
                chegada = processos['instanteChegada'][processo]
                duracao = processos['duracaoProcesso'][processo]
                prioridade = processos['prioridade'][processo]
                if (prioridade == processoMaiorP) and (duracao > 0) and (escolhido == False):
                    escolhido = True
                    if duracao - 1 != 0:
                        processos.loc[processo, 'prioridade'] = prioridade - 1
                        processos.loc[processo, 'duracaoProcesso'] = duracao - 1
                    else:
                        processos.drop(processo, inplace=True)
                else:
                    if duracao > 0:
                        processos.loc[processo, 'prioridade'] = prioridade + 1
        instante+=1

PrioridadesDinamicas(dados, 5)


