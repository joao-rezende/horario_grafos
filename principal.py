import networkx as nx
import matplotlib.pyplot as plt

class DataVertex(object):
    def __init__(self, id, subject, schoolClass, teacher):
        self.id, self.subject, self.schoolClass, self.teacher = id, subject, schoolClass, teacher
        self.adjacents = []

file = open("./public/files/dados.txt")

vertex = []
G = nx.Graph()

n = 0
for line in file:
    dados = line.split("|")
    numberClasses = int(dados[3].strip())
    for i in range(numberClasses):
        dataVertex = DataVertex(n, dados[0].strip(), dados[1].strip(), dados[2].strip())
        G.add_node(n)
        vertex.append(dataVertex)
        n += 1

for v1 in vertex:
    for v2 in vertex:
        if(v1.id != v2.id and (v1.subject == v2.subject or v1.teacher == v2.teacher)):
            v1.adjacents.append(v2)
            v2.adjacents.append(v1)
            G.add_edge(v1.id, v2.id)

pos = nx.circular_layout(G)

# Desenhando o grafo
nx.draw(G, pos, with_labels=True)
plt.show()