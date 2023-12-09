import networkx as nx

def graph_filtro_ano(ano):
    grafo_filtrado = dict()
    file = open(f"graph{ano}.txt", "rt", encoding="utf-8")
    for linha in file:
        dados = linha.split(";")
        if dados[0] not in grafo_filtrado:
            grafo_filtrado[dados[0]] = dict ()
        grafo_filtrado[dados[0]].update({dados[1]:int(dados[2])})
    file.close()
    return grafo_filtrado

def politicians_filtro_ano(ano):
    politicos_filtrado = dict ()
    file = open(f"politicians{ano}.txt", "rt", encoding="utf-8")
    for linha in file:
        dados = linha.split(";")
        if dados[0] not in politicos_filtrado:
            politicos_filtrado[dados[0]] = dict ()
        politicos_filtrado[dados[0]].update({"partido":dados[1], "qtd_votos":int(dados[2])})
    file.close()
    return politicos_filtrado



def cria_grafo(grafo_filtrado, politicos_filtrado):
    g = nx.Graph()
    for nome, votos in grafo_filtrado.items():
        partido = politicos_filtrado.get(nome, {}).get("partido", "")
        g.add_node(nome, partido=partido)
        for nome2, peso in votos.items():
            g.add_edge(nome, nome2, weight=peso)
    return g

def filtro_partido(g, politicos_filtrado, lista_partidos):
    politicos_para_remover = []
    for politico in g.nodes():
        if politico in politicos_filtrado:
            partido_politico = politicos_filtrado[politico]["partido"]
            if partido_politico not in lista_partidos:
                politicos_para_remover.append(politico)
    for politico in politicos_para_remover:
        g.remove_node(politico)
    return g

def normalizacao(g, politicos_filtrado):
    print(g)
    for no1,no2 in g.edges():
        edge_data = g.get_edge_data(no1,no2)
        if edge_data:
            peso = edge_data["weight"]
            votos_no1 = politicos_filtrado[no1]["qtd_votos"]
            votos_no2 = politicos_filtrado[no2]["qtd_votos"]
            peso_normalizado = peso / min(votos_no1, votos_no2)
            g[no1][no2]["weight"] = peso_normalizado
    return g

def threshold(g, threshold):
    if threshold > 0 and threshold <= 1:
        edges_to_remove = []
        for node1, node2 in list(g.edges):
            edge_data = g.get_edge_data(node1, node2)
            if edge_data:
                weight = edge_data["weight"]
                if weight <= 0 or weight > 1: 
                    return None
                if weight < threshold: 
                    edges_to_remove.append((node1, node2))
        for node1, node2 in edges_to_remove:
            g.remove_edge(node1, node2)
    return g

def inversao_peso(g):
    for node1, node2 in list(g.edges):
        edge_data = g.get_edge_data(node1, node2)
        if edge_data:
            weight = edge_data["weight"]
            if weight <= 0 or weight > 1: 
                return None
            g[node1][node2]["weight"] = 1 - weight
    return g
