import networkx as nx
import matplotlib.pyplot as plt

class VertexData(object):
    def __init__(self, vertexDataId, subject, schoolClass, teacher, classRestriction):
        self.vertexDataId, self.subject, self.schoolClass, self.teacher = vertexDataId, subject, schoolClass, teacher
        self.classRestriction = classRestriction
        self.adjacents, self.schedule_id, self.saturation = [], None, -1

# Gerando lista com os horários representando as cores
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

# Gerando lista de restrião de cada turma
fileRestriction = open("./public/files/restricoes_turma.txt")

allClassRestriction = []
for i in range(11):
    allClassRestriction.append([])
for line in fileRestriction:
    data = line.split("|")
    allClassRestriction[int(data[0]) - 1].append(schedules.index(data[1].strip()))

fileRestriction.close()

file = open("./public/files/dados_escola_A.txt")

vertex = []
vertexListId = []
G = nx.Graph()

n = 0
for line in file:
    data = line.split("|")
    numberClasses = int(data[3].strip())
    for i in range(numberClasses):
        vertexListId.append(n)
        vertexData = VertexData(n, data[0].strip(), data[1].strip(), data[2].strip(), allClassRestriction[int(data[1]) - 1])
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

notColoring = []
while(len(vertexListId) > 0):
    maxVertex = vertex[vertexListId[0]]
    for index in vertexListId:
        if(vertex[index].saturation > maxVertex.saturation or (vertex[index].saturation == maxVertex.saturation
            and len(vertex[index].adjacents) > len(maxVertex.adjacents))):
            maxVertex = vertex[index]

    color = 0
    colorValidate = False
    while(not colorValidate):
        colorValidate = True
        if(color in maxVertex.classRestriction):
            colorValidate = False
            color += 1
        else:
            for adjacent in maxVertex.adjacents:
                if(adjacent.schedule_id == color):
                    colorValidate = False
                    color += 1

    for adjacent in maxVertex.adjacents:
        adjacent.saturation += 1
    maxVertex.schedule_id = color

    vertexListId.remove(maxVertex.vertexDataId)

for v in vertex:
    if(v.schedule_id >= len(schedules)):
        notColoring.append(v.vertexDataId)

for s in range(len(schedules)):
    print(schedules[s])
    for v in vertex:
        if(v.schedule_id != None and v.schedule_id == s) :
            print("Matéria", v.subject, "/ ", v.teacher, "/ Turma", v.schoolClass)

print("Não coloridos: ")
for i in notColoring:
    v = vertex[i]
    print(v.schedule_id, " / Matéria", v.subject, "/ ", v.teacher, "/ Turma", v.schoolClass)