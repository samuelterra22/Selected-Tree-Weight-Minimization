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


def tem_ciclo(arco_candidato, V, lista_arestas):
    if arco_candidato[1] in V:
        return True
    return False


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
        melhor_aresta_positiva = None
        for e in aux:
            if not tem_ciclo(e, V, solucao_final):
                if e[2] <= 0:
                    solucao_final.append(e)
                    arestas_para_remover.append(e)
                    print(len(V), len(aux))
                    if e[1] not in V:
                        V.append(e[1])
                        ultimos_adicionados.append(e[1])
                else:
                    melhor_aresta_positiva = e
                    break
        for aresta in arestas_para_remover:
            aux.remove(aresta)
        if not ultimos_adicionados:
            delta = (n - len(V)) / n
            r = random.uniform(0, 1)
            if r < delta and melhor_aresta_positiva is not None:
                if melhor_aresta_positiva not in solucao_final:
                    solucao_final.append(melhor_aresta_positiva)
                solucao_final.append(melhor_aresta_positiva)
                if melhor_aresta_positiva[1] not in V:
                    V.append(melhor_aresta_positiva[1])
                    ultimos_adicionados.append(melhor_aresta_positiva[1])
                aux.remove(melhor_aresta_positiva)
            else:
                stop = True
    return solucao_final


def calcula_funcao_objetivo(solucao):
    return sum(x[2] for x in solucao)


if __name__ == '__main__':
    # Lê o arquivo de teste
    cab, arcs = le_arquivo('./testes/DAGs/1000_01_025_0.dag')
    s = resolve(0, arcs, cab[0])

    print(s)
    print(calcula_funcao_objetivo(s))
