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
    for v in V:
        if v == arco_candidato[1]:
            for e in lista_arestas:
                if e[0] == v:
                    if e[1] in V:
                        return True
    return False


def resolve(no_inicial, lista_de_arcos, tamanho):
    lista_de_arcos.sort(key=lambda tup: tup[2], reverse=False)

    stop = False
    solucao_final = []

    V = [no_inicial]
    aux = []
    ultimo_adicionado = no_inicial
    while not stop:
        for e in lista_de_arcos:
            if e[0] == ultimo_adicionado:
                aux.append(e)

        aux.sort(key=lambda tup: tup[2], reverse=False)

        for e in aux:
            if not tem_ciclo(e, V, lista_de_arcos):
                solucao_final.append(e)
                V.append(e[1])
                aux.remove(e)
                ultimo_adicionado = e[1]
                break

        if len(V) == tamanho:
            stop = True

    return solucao_final


def calcula_funcao_objetivo(solucao):
    return sum(x[2] for x in solucao)


if __name__ == '__main__':
    # Lê o arquivo de teste
    cab, arcs = le_arquivo('./testes/DAGs/100_01_050_0.dag')
    s = resolve(0, arcs, cab[1])

    print(s)
    print(calcula_funcao_objetivo(s))

