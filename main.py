import copy
import random

"""
Ideia principal do algoritmo:

O algoritmo inicialmente realiza leitura do arquivo de acordo com a instância
informada, retornando o cabeçalho com as configurações de entrada. 

Em seguida, com a função "resolve", 


O método "resolve" termina quando a lista de tarefas estiver vazia. 

Por fim, é calculado a função objetivo somando o peso de todos os arcos da árvore resultante.
"""


def le_arquivo(arquivo):
    """
    Função responsável por realizar a leitura da instância no arquivo.
    :param arquivo: Caminho do arquivo (instância)
    :return:        Retorna o cabeçalho contendo as duas primeiras linhas do arquivo
                    e a lista de arcos.
    """

    # Abre arquivo para leitura
    f = open(arquivo, "r")

    # Pega as linhas
    linhas = f.readlines()

    # Pega as duas primeiras linhas e joga numa lista
    cabecalho = [int(linhas[i].replace("\n", "")) for i in range(2)]

    # Lê as n linhas restantantes transformando os valores em inteiros e depois como tuplas de arcos (u, v, w)
    arcos = [tuple(map(int, linhas[i].replace("\n", "").split())) for i in range(2, len(linhas))]

    # Retorna o cabeçalho e a lista de arcos (u, v, w)
    return cabecalho, arcos[:len(arcos) - 1]


def resolve(no_inicial, lista_de_arcos, n):
    """
    Função Responsável por contruir a árvore direciona T a partir da lista de arcos
     que formam o grafo.
    :param no_inicial:      Id do vértice inicial do grafo.
    :param lista_de_arcos:  Lista de arcos vinda da instancia do arquivo.
    :param n:               Número de arcos contidos no grafo.
    :return:                Retorna o lits solução contendo a lista de arcos que
                            constituem a árvore direcionada T.
    """

    # Ordena a lista de arcos de forma crescente
    lista_de_arcos.sort(key=lambda tup: tup[2], reverse=False)

    # Variável de controle para parar laço principal
    stop = False

    # Lista para guardar a solução final de vertices
    solucao_final = []

    # Lista de vertices
    V = [no_inicial]

    # Vetores auxiliares para
    aux = []
    ultimos_adicionados = [no_inicial]
    while not stop:
        # Para todos da lista de arcos
        for e in lista_de_arcos:
            # E que o vertice de origem esta contino na lista de ultimos adicionados
            if e[0] in ultimos_adicionados:
                # Adiciona na lista auxiliar
                aux.append(e)

        # Ordena a lista auxiliar de arcos de forma crescente
        aux.sort(key=lambda tup: tup[2], reverse=False)

        # Vetor auxiliar para controle de parada do algoritmo
        ultimos_adicionados = []

        # Lista que irá conter arcos que serão removidas da lista auxiliar e lista de arcos
        arcos_para_remover = []

        # Para todas as arcos da lista auxiliar,
        for e in aux:
            # que não possuem ciclo
            if not tem_ciclo(e, V, solucao_final):
                # Se o peso da arco for negativo
                if e[2] <= 0:
                    # Adiciona a arco na solução final
                    solucao_final.append(e)
                    # Adiciona ela na lista de arcos a serem removidas
                    arcos_para_remover.append(e)

                    # Se o vertice de destino nao tiver sido visitado
                    if e[1] not in V:
                        # Adiciona o vertice de destino da arco, na lista de vertices
                        V.append(e[1])
                        # Adiciona o vertice na lista de ultimos adicionados
                        ultimos_adicionados.append(e[1])
                # Senão o peso da arco é positivo
                else:
                    # Cálcula o delta. O delta é um valor de 0.0 a 1.0, sendo que, quando mais próximo
                    # for o tamanho de V, mais o valor de delta estará próximo de zero
                    delta = (n - len(V)) / n
                    # Sorteia um número aleatório de 0 a 1
                    r = random.uniform(0, 1)
                    # Quanto maior a solução menor a probabilidade de adicionar um arco com peso positivo
                    # na lista de soluções
                    if r < delta:
                        # Adiciona o arco na lista de soluções
                        solucao_final.append(e)

                        # Se o vertice de destino nao tiver sido visitado
                        if e[1] not in V:
                            # Adiciona o vertice de destino da arco, na lista de vertices
                            V.append(e[1])
                            # Adiciona o vertice na lista de ultimos adicionados
                            ultimos_adicionados.append(e[1])
                        # Adiciona o arco na lista de arcos a serem removidos
                        arcos_para_remover.append(e)
                    break
        # Remove arcor
        for arco in arcos_para_remover:
            # Remove a arco da lista auxiliar de arcos
            aux.remove(arco)
            # Remove tambem da lista de arcos
            lista_de_arcos.remove(arco)
        # Verifica se a lista de últimos adicionados não está vazia,
        if not ultimos_adicionados:
            # Caso esteja vazia, para o laço de repetição e retorna a solução final
            stop = True

    # Retorna a lita solução com os arcos da árvore
    return solucao_final


def calcula_funcao_objetivo(solucao):
    """
    Função reponsável por realizar o cálculo da função objetivo.
    :param solucao: Solução como uma lista de arcos.
    :return:        Retorna o somatório de todos os pesos dos arcos da árvore.
    """
    return sum(x[2] for x in solucao)


def tem_ciclo_grafo_V2(arco_candidato, V):
    """
    Função versão mais simplificada para verificação de ciclo.
    :param arco_candidato:  Arco candidato (u, v, w) a ser verificado.
    :param V:               Lista de vértices.
    :return:                Retorna True se o vértice de destino do arco candidato
                            estiver contido na lista de vértices.
    """

    # Verifica se o vértice de destino está contido na lista de vértices.
    if arco_candidato[1] in V:
        return True
    return False


def tem_ciclo(arco_candidato, V, solucao):
    """
    Função para verificar se há ciclo no grafo ao adiciona um novo vértice no grafo.
    :param arco_candidato:  Arco candidato (u, v, w) a ser verificado.
    :param V:               Lista de vértices.
    :param solucao:         Lista de arcos da solução atual.
    :return:                Retorna False se for verificado um ciclo com o novo arco
                            adicionado, caso contrário, retorna True.
    """

    # Verifica se o vértice de destino do arco candidato nao está contido em V
    if arco_candidato[1] not in V:
        return False

    # Copia a lista de vértices V para uma lista auxiliar
    aux_V = copy.deepcopy(V)

    # Adiciona o vértice de destino do arco candidato na lista de vértices auxiliar
    aux_V.append(arco_candidato[1])
    # Faz uma cópia da lista solução
    arcos_arvore = copy.deepcopy(solucao)
    # E adiciona o arco candidato na lista de arcos da arvore
    arcos_arvore.append(arco_candidato)

    # Para todos os vértices
    for v in aux_V:
        # Retorna VERDADEIRO informando que há ciclo se possui um caminho de
        # retorno de v para as arcos da sulução
        if tem_caminho_retorno(v, arcos_arvore):
            return True
    # Se não possui caminho de retorno da lisya de vértices para os vértices da solução,
    # retorna FALSO informando que não há ciclos
    return False


def tem_caminho_retorno(v, solucao):
    """
    Função para verificar se possui caminho de retorno de uma lista de
    arcos para um vertice v.
    :param v:       Id do vértice.
    :param solucao: Lista de arcos.
    :return:        Returna True se tiver um caminho de retorno de algum
                    arco da lista para o vértice v.
    """
    # Lista para controle dos vértices visitados
    vertices_ja_visitados = []

    # Inicia pilha de controle com o vértice informado
    pilha = [v]

    # Enquando a pilha nao estiver vazia
    while pilha:
        # Retira o vértice do topo da pilha para a análise se há caminho de retorno
        vertice_atual = pilha.pop(0)

        # Para as todas as arcos na lista de solução
        for arco in solucao:
            # Verifica se o vertice atual é o mesmo vértice de origem da arco da
            # lista de soluções, checando se o vértice atual tem uma arco pra alguem,
            if vertice_atual == arco[0]:
                #  Se tiver arco e ela não foi visitada, adiciona na pilha
                if arco[1] not in vertices_ja_visitados:
                    pilha.append(arco[1])

                # Se possui uma arco na solução que volta para onde começou,
                # retorna VERDADEIRO saindo do método e informando que possue um caminho
                # de retono
                if arco[1] == v:
                    return True
        # Depois de verificar caminho de retorno para todas as soluções,
        # adiciona o vértice atual na lista de vertices visitados
        vertices_ja_visitados.append(vertice_atual)

    # Caso não possua caminho de retorno, retorna FALSO
    return False


if __name__ == '__main__':
    # Lê o arquivo da instancia
    cab, arcos = le_arquivo('./instances/DAGs/100_01_050_0.dag')

    # Constroe a árvore direcionada T a partir do primeiro vértice com os
    # dados do arquivo de entrada
    T = resolve(0, arcos, cab[0])

    print(T)
    print(calcula_funcao_objetivo(T))
