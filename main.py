import copy
import random


def le_arquivo(arquivo):
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
    lista_de_arcos.sort(key=lambda tup: tup[2], reverse=False)

    stop = False
    solucao_final = []

    V = [no_inicial]
    aux = []
    ultimos_adicionados = [no_inicial]
    while not stop:
        for e in lista_de_arcos:
            if e[0] in ultimos_adicionados:
                aux.append(e)
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
    return solucao_final


def calcula_funcao_objetivo(solucao):
    return sum(x[2] for x in solucao)


def tem_ciclo_grafo_V2(arco_candidato, V):
    if arco_candidato[1] in V:
        return True
    return False


def tem_ciclo(arco_candidato, V, solucao):
    if arco_candidato[0] not in V:
        return False
    aux_V = copy.deepcopy(V)
    aux_V.append(arco_candidato[1])
    arestas_arvore = copy.deepcopy(solucao)
    arestas_arvore.append(arco_candidato)
    for v in aux_V:
        if tem_caminho_retorno(v, arestas_arvore):
            return True
    return False


def tem_caminho_retorno(v, solucao):
    vertices_ja_visitados = []
    pilha = [v]
    while pilha:
        vertice_atual = pilha.pop(0)
        for aresta in solucao:
            if vertice_atual == aresta[0]:
                if aresta[1] not in vertices_ja_visitados:
                    pilha.append(aresta[1])
                if aresta[1] == v:
                    return True
        vertices_ja_visitados.append(vertice_atual)
    return False


if __name__ == '__main__':
    # Lê o arquivo de teste
    cab, arcs = le_arquivo('./testes/DAGs/100_01_050_0.dag')
    s = resolve(0, arcs, cab[0])

    print(s)
    print(calcula_funcao_objetivo(s))

    # V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # grafo = [
    #     (0, 1, 0), (0, 2, 0), (0, 7, 0), (4, 5, 0), # (3, 5, 0),
    #     (2, 4, 0), (5, 6, 0), (7, 6, 0), (7, 8, 0), (8, 6, 0),
    #     (6, 9, 0), (8, 9, 0), (1, 3, 0), (4, 3, 0), (4, 8, 0),
    #     (6, 1, 0)
    # ]
    # print(tem_ciclo(None, V, grafo))
