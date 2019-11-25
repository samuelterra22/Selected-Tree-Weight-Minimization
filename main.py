import copy
import random


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
    :return:                Retorna o vetor solução contendo a lista de arcos que
                            constituem a árvore direcionada T.
    """

    # Ordena a lista de arcos de forma crescente
    lista_de_arcos.sort(key=lambda tup: tup[2], reverse=False)

    # Variável de controle para parar laço principal
    stop = False
    solucao_final = []

    V = [no_inicial]
    aux = []
    ultimos_adicionados = [no_inicial]
    while not stop:
        for e in lista_de_arcos:
            if e[0] in ultimos_adicionados:
                aux.append(e)

        # Ordena novamente a lista de arcos de forma crescente
        aux.sort(key=lambda tup: tup[2], reverse=False)
        ultimos_adicionados = []
        arestas_para_remover = []
        for e in aux:
            if not tem_ciclo(e, V, solucao_final):
                if e[2] <= 0:
                    solucao_final.append(e)
                    arestas_para_remover.append(e)
                    if e[1] not in V:
                        V.append(e[1])
                        ultimos_adicionados.append(e[1])
                else:
                    delta = (n - len(V)) / n
                    r = random.uniform(0, 1)
                    if r < delta:
                        solucao_final.append(e)
                        if e[1] not in V:
                            V.append(e[1])
                            ultimos_adicionados.append(e[1])
                        arestas_para_remover.append(e)
                    break
        for aresta in arestas_para_remover:
            aux.remove(aresta)
            lista_de_arcos.remove(aresta)
        if not ultimos_adicionados:
            stop = True

    # Retorna o vetor solução com os arcos da árvore
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

    # Verifica se o vértice de destino está contino na lista de vértices.
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

    # Verifica se o vértice de origem do arco candidato nao está contido em V
    if arco_candidato[0] not in V:
        return False

    # Copia o vetor de vértices V para um vetor auxiliar
    aux_V = copy.deepcopy(V)

    # Adiciona o vértice de destino do arco candidato na lista de vértices auxiliar
    aux_V.append(arco_candidato[1])
    arestas_arvore = copy.deepcopy(solucao)
    arestas_arvore.append(arco_candidato)

    # Para todos os vértices
    for v in aux_V:
        # Retorna VERDADEIRO informando que há ciclo se possui um caminho de
        # retorno de v para as arestas da sulução
        if tem_caminho_retorno(v, arestas_arvore):
            return True
    # Se não possui caminho de retorno do vetor de vértices para os vértices da solução,
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

        # Para as todas as arestas na lista de solução
        for aresta in solucao:
            # Verifica se o vertice atual é o mesmo vértice de origem da aresta da
            # lista de soluções, checando se o vértice atual tem uma aresta pra alguem,
            if vertice_atual == aresta[0]:
                #  Se tiver aresta e ela não foi visitada, adiciona na pilha
                if aresta[1] not in vertices_ja_visitados:
                    pilha.append(aresta[1])

                # Se possui uma aresta na solução que volta para onde começou,
                # retorna VERDADEIRO saindo do método e informando que possue um caminho
                # de retono
                if aresta[1] == v:
                    return True
        # Depois de verificar caminho de retorno para todas as soluções,
        # adiciona o vértice atual na lista de vertices visitados
        vertices_ja_visitados.append(vertice_atual)

    # Caso não possua caminho de retorno, retorna FALSO
    return False


if __name__ == '__main__':
    # Lê o arquivo da instancia
    cab, arcos = le_arquivo('./testes/DAGs/100_01_050_0.dag')

    # Constroe a árvore direcionada T a partir do primeiro vértice com os
    # dados do arquivo de entrada
    T = resolve(0, arcos, cab[0])

    print(T)
    print(calcula_funcao_objetivo(T))
