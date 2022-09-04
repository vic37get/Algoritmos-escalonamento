# Execução
`python3 [nomeDoArquivo].py < entrada.txt`

## Funcionamento
* Tempo de retorno médio – Refere-se ao tempo transcorrido entre o momento da entrada do processo no sistema e o seu término.
* Tempo de resposta médio – Intervalo de tempo entre a chegada do processo e o início de sua execução.
* Tempo de espera médio – Soma dos períodos em que um processo estava no seu estado pronto.

## Entrada
A entrada é composta por uma série de pares de números inteiros separadas por um espaço em branco indicando o instante de chegada do processo e a duração de cada processo.

### Exemplo de entrada

Instante de chegada | Duração do processo
-- | --
0 | 2
0 | 3
1 | 2
1 | 4

## Saída
A saída é composta por linhas contendo a sigla de cada um dos três algoritmos e os valores das
três métricas solicitadas. Cada linha apresenta a sigla do algoritmo e os valores médios (com
uma casa decimal) para tempo de retorno, tempo de resposta e tempo de espera, exatamente
nesta ordem, separados por um espaço em branco.

### Exemplo de saída

Algoritmo | Tempo de retorno médio | Tempo de resposta médio | Tempo de espera médio |
-- | -- | -- | -- |
PRI | 7.50 | 1.00 | 4.75 |
LOT | 7.00 | 2.50 | 4.25 |
RR | 6.50 | 2.50 | 3.75 |
