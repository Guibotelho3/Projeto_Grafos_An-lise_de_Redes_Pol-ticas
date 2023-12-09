import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import random

def plot_grafo(g, filename):
    cor_mapa = dict()
    cor_nos = list()
    paleta_cores = plt.cm.tab20.colors
    cores_usadas = set()
    for n in g.nodes():
        if g.nodes[n]["partido"] not in cor_mapa:
            while True:
                cor = random.choice(paleta_cores)
                if cor not in cores_usadas:
                    cor_mapa[g.nodes[n]["partido"]] = cor
                    cores_usadas.add(cor)
                    break
        cor_nos.append(cor_mapa[g.nodes[n]["partido"]])
    
    # Plota o grafo
    figure = Canvas(plt.figure())
    plt.title('Grafo')
    positions = nx.spring_layout(g)
    nx.draw(g, positions, node_size=100, node_color=cor_nos, width=1, with_labels=True, font_size=10)
    
    # Cria uma legenda com as cores dos partidos
    for partido, cor in cor_mapa.items():
        plt.scatter([], [], c=[cor], label=partido)
    plt.legend()
    figure.draw()
    plt.savefig(filename)
    return figure

def plot_centralidade(g, filename):
    centralidade = nx.betweenness_centrality(g)
    centralidade = sorted(centralidade.items(), key=lambda x: x[1])
    keys, values = zip(*centralidade)
    keys = list(keys)
    for i in range(len(keys)):
            keys[i] += " (" + g.nodes[keys[i]]['partido'] + ")"

    # Plotar o gráfico de centralidade
    figure = Canvas(plt.figure())
    plt.title('Centralidade')
    plt.bar(keys, values, align='center')
    plt.xticks(rotation=45, ha="right", fontsize=6)
    plt.xlabel('Deputados')
    plt.ylabel('Centralidade')
    plt.tight_layout()
    figure.draw()
    plt.savefig(filename)
    return figure

def plot_heatmap(g, filename):
    deputados = sorted(list(g.nodes))
    correlacao = np.zeros((len(deputados), len(deputados)))
    for i, dep1 in enumerate(deputados):
        for j, dep2 in enumerate(deputados):
            if i == j:
                correlacao[i, j] = 1
            else:
                if g.has_edge(dep1, dep2):
                    correlacao[i, j] = g[dep1][dep2]['weight']
    for i in range(len(deputados)):
            deputados[i] = (deputados[i], g.nodes[deputados[i]]['partido'])
    deputados = sorted(deputados, key=lambda x: x[1])
    for i in range(len(deputados)):
            deputados[i] = deputados[i][0] + ' (' + deputados[i][1] + ')'

    # Plotar o heatmap
    figure = Canvas(plt.figure())
    plt.title('HeatMap')
    plt.imshow(correlacao, cmap='coolwarm', interpolation='none', aspect='auto')
    plt.xticks(range(len(deputados)), deputados, rotation=45, ha="right", fontsize=6)
    plt.yticks(range(len(deputados)), deputados, fontsize=6)
    plt.colorbar(label='Nível de Correlação')
    plt.tight_layout()
    figure.draw()
    plt.savefig(filename)
    return figure