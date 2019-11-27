import networkx as nx
import matplotlib.pyplot as plt

class VertexData(object):
    def __init__(self, vertexDataId, subject, schoolClass, teacher):
        self.vertexDataId, self.subject, self.schoolClass, self.teacher = vertexDataId, subject, schoolClass, teacher
        self.adjacents, self.schedule_id, self.saturation = [], None, -1

file = open("./public/files/dados_escola_A.txt")

vertex = []
vertexListId = []
G = nx.Graph()

n = 0
for line in file:
    dados = line.split("|")
    numberClasses = int(dados[3].strip())
    for i in range(numberClasses):
        vertexListId.append(n)
        vertexData = VertexData(n, dados[0].strip(), dados[1].strip(), dados[2].strip())
        G.add_node(n)
        vertex.append(vertexData)
        n += 1

file.close()

for v1 in vertex:
    for v2 in vertex:
        if(v1.vertexDataId != v2.vertexDataId and (v1.schoolClass == v2.schoolClass or v1.teacher == v2.teacher)):
            v1.adjacents.append(v2)
            v2.adjacents.append(v1)
            G.add_edge(v1.vertexDataId, v2.vertexDataId)

file = open("./public/files/horarios_escola_A.txt")

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
while(len(vertexListId) > 0):
    maxVertex = vertex[vertexListId[0]]
    for index in vertexListId:
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
        notColoring.append(maxVertex.vertexDataId)

    vertexListId.remove(maxVertex.vertexDataId)

print(notColoring)

for s in range(len(schedules)):
    print(schedules[s])
    for v in vertex:
        if(v.schedule_id != None and v.schedule_id == s) :
            print("Matéria", v.subject, "/ ", v.teacher, "/ Turma", v.schoolClass)