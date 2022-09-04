# Execução
`python3 [nomeDoArquivo].py < entrada.txt`

## Funcionamento
O programa lê da entrada padrão um conjunto de números inteiros onde o primeiro número representa a quantidade de cilindros no disco, o segundo número representa o cilindro sobre o qual a cabeça de leitura do disco está inicialmente posicionada e os demais representam uma sequência de requisições de acesso a serem atendidas, sempre um número por linha. 

O programa imprime na saída o número total de cilindros percorridos pela cabeça de leitura para atender todas as requisições solicitadas utilizando cada um dos algoritmos.

## Entrada
A entrada é composta por uma série de números inteiros, um por linha, indicando primeiro o número do último cilindro no disco (os cilindros variam de 0 até este número), o cilindro sobre o qual a cabeça de leitura está inicialmente posicionada e a sequência de requisições de acesso.

### Exemplo de entrada
199
53
98
183
37
122
14
124
65
67

## Saída
A saída é composta por linhas contendo a sigla de cada um dos três algoritmos e a quantidade total de cilindros percorridos pela cabeça de leitura para atender todas as requisições de acesso ao disco

### Exemplo de saída

Algoritmo | Quantidade de cilíndros percorridos |
-- | -- |
FCFS | 640 |
SSTF | 236 |
ELEVADOR | 299 |
