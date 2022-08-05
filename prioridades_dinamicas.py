import sys

from numpy import ones

arquivo = sys.stdin
dados = arquivo.readlines()

instante_chegada = []
duracao_processo = []
processos = list(range(0, len(dados)))
prioridades = list()

for linha in dados:
    instante_chegada.append(linha[0])
    duracao_processo.append(linha[2])



