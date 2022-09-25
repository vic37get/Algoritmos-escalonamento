import copy

import pandas as pd


def TratamentoArquivoRR(arquivo):
    dados = copy.deepcopy(arquivo)
    for linha in range(len(dados)):
        dados[linha] = dados[linha].replace('\n','').split()
        dados[linha] = dados[linha] + list(dados[linha][-1])
        dados[linha].append(linha)
        dados[linha].append(linha+1)
        dados[linha].append(0)
        dados[linha].append(0)
    df = pd.DataFrame(dados, columns=['chegada', 'duracao', 'duracaoInicial', 'PID', 'posicao', 'executado', 'status'])
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
def EsperaMedio(instanteChegada, instanteTermino, duracaoTotal, qtd_processos):
    tempo_medio = []
    for processo in range(qtd_processos):
        tempo_medio.append(instanteTermino[processo] - instanteChegada[processo] - duracaoTotal[processo])
    return sum(tempo_medio)/qtd_processos

def roundRobin(dados):
    print('\n--Algoritmo RoundRobin--\n')
    #Retorno médio #Espera Médio
    instanteTermino, instanteChegada, duracaoProcesso = [], [], []
    #Resposta média
    chegadaProcesso, executadoProcesso = [], []
    #Instante atual
    instante = 0
    processos = TratamentoArquivoRR(dados)
    duracao_total = sum(processos['duracao'])
    #Enquanto o instante atual não for maior ou igual a duração total dos processos.
    while duracao_total != 0:
        #Ordenando a fila de processos pela posição de chegada do processo na fila.
        processos = processos.sort_values(by=['posicao'])
        #Processos candidatos à execução
        processos_candidatos = processos[(processos['chegada'] <= instante) & (processos['status'] != 1)]
        print('Instante', instante)
        print('Processos:\n',processos)
        print('Processos candidatos:\n', processos_candidatos)
        #Se há pelo menos um processo no estado pronto.
        if len(processos_candidatos) > 0:
            #Obtem o primeiro processo da fila
            processo = processos_candidatos.iloc[0]
            print('Processo escolhido: \n', processos[processos['PID'] == processo['PID']])
            duracao = processo['duracao']
            chegada = processo['chegada']
            PID = processo['PID']
            executado = processo['executado']
            print('Duracao: ', duracao)
            #Se o processo está sendo executado pela primeira vez
            if executado != 1:
                chegadaProcesso.append(chegada)
                executadoProcesso.append(instante)
                processos.loc[processos.PID == PID, 'executado'] = 1
            #Se a duração do processo ainda for maior ou igual a um quantum:
            if duracao - 2 >= 0:
                duracao-=2
                processos.loc[processos.PID == PID, 'duracao'] = duracao
                print('Processo após executar:\n', processos[processos['PID'] == processo['PID']])
                duracao_total-=2
                instante+=2
            #Se a duração for igual a 1:
            else:
                duracao-=1
                processos.loc[processos.PID == PID, 'duracao'] = duracao
                print('Processo após executar:\n', processos[processos['PID'] == processo['PID']])
                duracao_total-=1
                instante+=1
            #Se o processo já finalizou sua execução.
            if duracao == 0:
                processos.loc[processos.PID == PID, 'status'] = 1
                instanteChegada.append(chegada)
                instanteTermino.append(instante)
                duracaoProcesso.append(processo['duracaoInicial'])
            #Se o processo ainda não finalizou sua execução.
            else:
                #Obtem a posição do ultimo da fila
                ultimoDaFila = processos['posicao'].max()
                #Coloca o processo na ultima posição da fila
                processos.loc[processos.PID == PID, 'posicao'] = ultimoDaFila + 1
        #Se não há processos no estado pronto.
        else:
            print(processos_candidatos)
            print('O processador está ocioso')
            instante+=1

    retorno_md = RetornoMedio(instanteChegada, instanteTermino)
    resposta_md = RespostaMedia(chegadaProcesso, executadoProcesso)
    espera_md = EsperaMedio(instanteChegada, instanteTermino, duracaoProcesso, len(processos))

    return retorno_md, resposta_md, espera_md
