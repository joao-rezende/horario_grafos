import networkx as nx
import matplotlib.pyplot as plt

class DataVertex(object):
    def __init__(self, dataVertexId, subject, schoolClass, teacher):
        self.dataVertexId, self.subject, self.schoolClass, self.teacher = dataVertexId, subject, schoolClass, teacher
        self.adjacents, self.schedule_id, self.saturation = [], None, -1

file = open("./public/files/dados_teste.txt")

vertex = []
listVertexId = []
G = nx.Graph()

n = 0
for line in file:
    dados = line.split("|")
    numberClasses = int(dados[3].strip())
    for i in range(numberClasses):
        listVertexId.append(n)
        dataVertex = DataVertex(n, dados[0].strip(), dados[1].strip(), dados[2].strip())
        G.add_node(n)
        vertex.append(dataVertex)
        n += 1

file.close()

for v1 in vertex:
    for v2 in vertex:
        if(v1.dataVertexId != v2.dataVertexId and (v1.subject == v2.subject or v1.teacher == v2.teacher)):
            v1.adjacents.append(v2)
            v2.adjacents.append(v1)
            G.add_edge(v1.dataVertexId, v2.dataVertexId)

file = open("./public/files/horarios_teste.txt")

days_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
hours = []
schedules = []

for line in file:
    hours.append(line.strip())

for day in days_week:
    for hour in hours:
        schedules.append("{} - {}".format(day, hour))

file.close()

notColoring = []
while(len(listVertexId) > 0):
    maxVertex = vertex[listVertexId[0]]
    for index in listVertexId:
        if(vertex[index].saturation > maxVertex.saturation or (vertex[index].saturation == maxVertex.saturation
            and len(vertex[index].adjacents) > len(maxVertex.adjacents))):
            maxVertex = vertex[index]

    color = 0
    colorValidate = False
    while(color < len(schedules) and not colorValidate):
        colorValidate = True
        for adjacent in maxVertex.adjacents:
            if(adjacent.schedule_id == color):
                colorValidate = False
                color += 1

    if(color < len(schedules)):
        for adjacent in maxVertex.adjacents:
            adjacent.saturation += 1
        maxVertex.schedule_id = color
    else:
        notColoring.append(maxVertex.dataVertexId)

    listVertexId.remove(maxVertex.dataVertexId)

print(notColoring)

for v in vertex:
    if(v.schedule_id != None) :
        print("Horário: ", schedules[v.schedule_id])
        print("Matéria: ", v.subject)
        print("Professor: ", v.teacher)
        print("Turma: ", v.schoolClass)