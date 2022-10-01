import sys

import loteria as lot
import prioridades as pri
import roundRobin as rr


def OpenFile():
    arquivo = sys.stdin
    try:
        dados = arquivo.readlines()
        return dados
    except:
        print('Arquivo não encontrado!')
        exit(0)


dados = OpenFile()

def Execução():
    retornoMedio_pri, respostaMedia_pri, esperaMedia_pri = pri.PrioridadesDinamicas(dados, 5)
    retornoMedio_lot, respostaMedia_lot, esperaMedia_lot = lot.Loteria(dados)
    retornoMedio_rr, respostaMedia_rr, esperaMedia_rr = rr.roundRobin(dados)
    print('PRI %.2f %.2f %.2f' %(retornoMedio_pri, respostaMedia_pri, esperaMedia_pri))
    print('LOT %.2f %.2f %.2f' %(retornoMedio_lot, respostaMedia_lot, esperaMedia_lot))
    print('RR %.2f %.2f %.2f' %(retornoMedio_rr, respostaMedia_rr, esperaMedia_rr))

#Passo a passo
def ExecuçãoPassoApasso():
    retornoMedio_pri, respostaMedia_pri, esperaMedia_pri = pri.PrioridadesDinamicasPassoApasso(dados, 5)
    retornoMedio_lot, respostaMedia_lot, esperaMedia_lot = lot.LoteriaPassoApasso(dados)
    retornoMedio_rr, respostaMedia_rr, esperaMedia_rr = rr.roundRobinPassoApasso(dados)
    print('PRI %.2f %.2f %.2f' %(retornoMedio_pri, respostaMedia_pri, esperaMedia_pri))
    print('LOT %.2f %.2f %.2f' %(retornoMedio_lot, respostaMedia_lot, esperaMedia_lot))
    print('RR %.2f %.2f %.2f' %(retornoMedio_rr, respostaMedia_rr, esperaMedia_rr))

###########
#Chamada do "main"
#ExecuçãoPassoApasso()
Execução()
