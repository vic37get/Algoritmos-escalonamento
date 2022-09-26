import copy
import random

import pandas as pd


def TratamentoArquivoLot(arquivo):
    dados = copy.deepcopy(arquivo)
    for linha in range(len(arquivo)):
        dados[linha] = dados[linha].replace('\n','').split()
        dados[linha] = dados[linha] + list(dados[linha][-1])
        dados[linha].append(linha)
        dados[linha].append(0)
        dados[linha].append(0)
    df = pd.DataFrame(dados, columns=['chegada', 'duracao', 'duracaoInicial', 'PID', 'executado', 'status'])
    df = df.astype(int)
    return df

#Escolhe um processo de forma aleatória a partir do seu PID
def EscolheProcesso(processos_candidatos):
    PID_PROCESSO = random.choice(processos_candidatos['PID'].values.tolist())
    processo = processos_candidatos.loc[PID_PROCESSO]
    return processo

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
def EsperaMedio(instanteChegada, instanteTermino, duracaoTotal, qtd_processos):
    tempo_medio = []
    for processo in range(qtd_processos):
        tempo_medio.append(instanteTermino[processo] - instanteChegada[processo] - duracaoTotal[processo])
    return sum(tempo_medio)/qtd_processos

def Loteria(dados):
    #Retorno médio #Espera Médio
    instanteTermino, instanteChegada, duracaoProcesso = [], [], []
    #Resposta média
    chegadaProcesso, executadoProcesso = [], []
    #Instante atual
    instante = 0
    #Processos
    processos = TratamentoArquivoLot(dados)
    duracao_total = sum(processos['duracao'])
    #Enquanto o instante atual não for maior ou igual a duração total dos processos.
    while duracao_total !=0:
        #Processos candidatos à execução
        processos_candidatos = processos[(processos['chegada'] <= instante) & (processos['status'] != 1)]
        print('\nInstante: {}'.format(instante))
        print('\nProcessos:\n {}\n'.format(processos))
        print('Processos candidatos:\n', processos_candidatos)
        #Se há pelo menos um processo no estado pronto.
        if len(processos_candidatos) > 0:
            processo = EscolheProcesso(processos_candidatos)
            print('\nProcesso escolhido: \n', processos[processos['PID'] == processo['PID']])
            duracao = processo['duracao']
            chegada = processo['chegada']
            PID = processo['PID']
            executado = processo['executado']

            #Se o processo está sendo executado pela primeira vez
            if executado != 1:
                chegadaProcesso.append(chegada)
                executadoProcesso.append(instante)
                processos.loc[processos.PID == PID, 'executado'] = 1

            #O processo vai executar
            duracao -=1 
            processos.loc[processos.PID == PID, 'duracao'] = duracao
            #Duração total da execução de todos os processos
            duracao_total -=1
            #Instante de execução
            instante+=1
            
            #Se o processo chegar ao seu fim.
            if duracao == 0:
                #Status finalizado
                processos.loc[processos.PID == PID, 'status'] = 1
                instanteChegada.append(chegada)
                instanteTermino.append(instante)
                duracaoProcesso.append(processo['duracaoInicial'])
            print('\nProcesso após executar:\n', processos[processos['PID'] == processo['PID']])
        
        else:
            print(processos_candidatos)
            print('\n--O processador está ocioso!--\n')
            instante+=1
        print('\n*******************************************************************************')
            
    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(instanteChegada, instanteTermino, duracaoProcesso, len(processos))

    return retorno_md, resposta_md, espera_md
