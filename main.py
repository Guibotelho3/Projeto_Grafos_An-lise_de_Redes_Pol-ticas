import processamento
import plot



print("Informe o ano a se considerar (de 2002 a 2023):")
ano_desejado = int(input())
gg = processamento.graph_filtro_ano(ano_desejado)
pp = processamento.politicians_filtro_ano(ano_desejado)
G = processamento.cria_grafo(gg,pp)

partidos_desejados = []
print("Digite os partidos a serem filtrados (separados por espaço): ")
partidos_desejados = input()
lista_partidos = partidos_desejados.split()
G1 = processamento.filtro_partido(G, pp, lista_partidos)

G2 = processamento.normalizacao(G1,pp)

print("Informe o percentual mínimo de concordância ( threshold ) ( ex . 0.9) :")
thresh = float(input())
G3 = processamento.threshold(G2,thresh)

G4 = processamento.inversao_peso(G3)

print("Processando.....")

plot.plot_grafo(G4, 'plot_grafo.png')
plot.plot_centralidade(G4, 'plot_centralidade.png')
plot.plot_heatmap(G4, 'plot_heatmap.png')

print(f"As vizualizações do grafo referente ao ano {ano_desejado}\nforam plotadas nos arquivos:")
print('plot_grafo.png')
print('plot_centralidade.png')
print('plot_heatmap.png')
print("Encontre-as no diretório do arquivo")
