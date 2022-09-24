import matplotlib.pyplot as plt


def GeraGrafico(tempo_total, qntd_process, mudança):
    fig, gnt = plt.subplots() 
    gnt.set_ylim(0, 100) 
    gnt.set_xlim(0, tempo_total) 
    gnt.set_xlabel('tempo') 
    gnt.set_ylabel('Processos') 
    gnt.grid(True)
    inicio_final = [(10,50),(20,100),(50,200),(0,200)]
    posicao = [(70,9),(50,9),(30,9),(10,9)]
    cor = ['tab:blue', 'tab:red','tab:green', 'tab:orange']
    for processos in range(qntd_process+1):
        gnt.broken_barh([inicio_final[processos]], posicao[processos], facecolors = cor[processos])
    fig.show()


for i in range(0,5):
    GeraGrafico(500, 3, i*10)