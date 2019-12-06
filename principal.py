
import openpyxl

class VertexData(object):
    def __init__(self, vertexDataId, subject, schoolClass, teacher, classRestriction, teacherRestriction):
        self.vertexDataId, self.subject, self.schoolClass, self.teacher = vertexDataId, subject, schoolClass, teacher
        self.classRestriction = classRestriction
        self.teacherRestriction = teacherRestriction
        self.adjacents, self.schedule_id, self.saturation = [], None, -1

#Abrindo a planilha
# path = "/home/desenvolvedor2/Documentos/Python/horario_grafos/public/files/Escola_A.xlsx"
path = "./public/files/Escola_A.xlsx"
wbObj = openpyxl.load_workbook(path)

schollData = wbObj['Dados']
settings = wbObj['Configuracoes']
classRestriction = wbObj['Restricoes Turma']
teacherRestriction = wbObj['Restricao']

# instanciando lista com os horários representando as cores
days_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
schedules = []

for day in days_week:
    jump = True
    for i, row in enumerate(settings.rows):
        if(i > 0):
            schedules.append("{} - {}".format(day, row[0].value))

# instanciando lista de restrição de cada turma e de cada professor
classes = []
teachers = []
#Colocando o os professores e turmas em uma lista
for i, row in enumerate(schollData.rows):
    if(i > 0):
        if (not row[0].value in classes):
            classes.append(row[0].value)

        if (not row[2].value in classes):
            teachers.append(row[2].value)

# Adicionado as restrições da turma e dos professores do arquivo em uma lista e 
# dicionário, respectivamente
allClassRestriction = []
for i in range(len(classes)):
    allClassRestriction.append([])

for i, row in enumerate(classRestriction.rows):
    if(i > 0):
        scheduleRestriction = "{} - {}".format(row[2].value, row[1].value)
        allClassRestriction[int(row[0].value) - 1].append(schedules.index(scheduleRestriction))

allTeacherRestriction = {}
for teacher in teachers:
    allTeacherRestriction[teacher] = []

for i, row in enumerate(teacherRestriction.rows):
    if(i > 0):
        scheduleRestriction = "{} - {}".format(row[2].value, row[1].value)
        allTeacherRestriction[row[0].value].append(schedules.index(scheduleRestriction))

# instanciando o grafo
vertex = []
vertexListId = []

n = 0

# Criando os vértices e adicionando todos os vértices em uma lista
# Cria um vértice com os um identificador, matéria, turma, professor,
# lista com restrição da turma e lista com restrição do professor.
# De acordo com a quantidade de aulas desta matéria, com o mesmo professor e turma
# e criado um vértice com as mesmas informações
for i, row in enumerate(schollData.rows):
    if(i > 0):
        numberClasses = int(row[3].value)
        for i in range(numberClasses):
            vertexListId.append(n)
            vertexData = VertexData(n, row[0].value, row[1].value, row[2].value, allClassRestriction[int(row[1].value) - 1], allTeacherRestriction[row[2].value])
            vertex.append(vertexData)
            n += 1

# Criando as arestas do grafo.
# Adiciona os vértices vizinhos em uma lista contendo os vértices adjacente do mesmo.
for v1 in vertex:
    for v2 in vertex:
        if(v1.vertexDataId != v2.vertexDataId and (v1.schoolClass == v2.schoolClass or v1.teacher == v2.teacher)):
            v1.adjacents.append(v2)
            v2.adjacents.append(v1)

# Algoritmo de coloração feito com base no algoritmo de Dsatur
colors = []
while(len(vertexListId) > 0):
    # Primeiro realiza uma busca para pegar o vértice com o maior número de saturação
    # ou caso o maior valor de saturação seja repetido com o maior grau.
    maxVertex = vertex[vertexListId[0]]
    for index in vertexListId:
        if(vertex[index].saturation > maxVertex.saturation or (vertex[index].saturation == maxVertex.saturation
            and len(vertex[index].adjacents) > len(maxVertex.adjacents))):
            maxVertex = vertex[index]

    # Colorindo o vértice com a menor cor possível, levando em consideração a restrição
    # de horário da turma e do professor e que nenhum dos seus adjacentes tenha a mesma
    # cor.
    color = 0
    colorValidate = False
    while(not colorValidate):
        colorValidate = True
        if(color in maxVertex.classRestriction or color in maxVertex.teacherRestriction):
            colorValidate = False
            color += 1
        else:
            for adjacent in maxVertex.adjacents:
                if(adjacent.schedule_id == color):
                    colorValidate = False
                    color += 1

    maxVertex.schedule_id = color
    # Aumentando o grau de saturação dos vértices adjacentes ao vértice pintado
    for adjacent in maxVertex.adjacents:
        adjacent.saturation += 1

    # Adicionando em uma lista as cores utilizadas na coloração dos vértices
    if(not color in colors):
        colors.append(color)

    # Remove da lista de vértices ainda não coloridos o vértice que foi colorido
    vertexListId.remove(maxVertex.vertexDataId)

# Realiza por duas vezes um algoritmo de melhoramento
for i in range(2):
    newColors = colors
    colors = []
    # Faz um laço com todas as cores que estão sendo usadas no grafo
    for c in newColors:
        for v in vertex:
            # Caso o vértice tenha a cor que está sendo considerada, busca
            # qual a menor cor que o vértice pode ter em relação as cores que estão sendo utilizadas
            if(c == v.schedule_id):
                i = 0
                colorfulVertex = False
                while ( i < len(newColors) or not colorfulVertex):
                    c2 = newColors[i]
                    if(not c2 in v.classRestriction and not c2 in v.teacherRestriction and c2 != v.schedule_id):
                        colorValidate = True
                        for adj in v.adjacents:
                            if(adj.schedule_id == c2):
                                colorValidate = False

                        # Troca a cor do vértice e indica que ele foi colorido para parar o loop
                        if(colorValidate):
                            v.schedule_id = c2
                            colorfulVertex = True

                        # Adiciona a nova cor usada na lista de cores
                        if(not v.schedule_id in colors):
                            colors.append(v.schedule_id)
                    i += 1

# Gera uma lista com a cores que estão sendo usadas pelos vértices
colors = []
for v in vertex:
    if(not v.schedule_id in colors):
        colors.append(v.schedule_id)

print("Número de cores:", len(colors))

# Exibe no tela os vértices, separados pelo horário (cor)
notColoring = []
for i, color in enumerate(colors):
    if(i < len(schedules)):
        print(schedules[i])
        for v in vertex:
            if(v.schedule_id == color) :
                print(v.schedule_id, " / Matéria", v.subject, "/ ", v.teacher, "/ Turma", v.schoolClass)
    else:
        notColoring.append(v)

# Exibe na tela os vértices que não foram coloridos
print("Não coloridos: ")
for i in notColoring:
    v = vertex[i]
    print(v.schedule_id, " / Matéria", v.subject, "/ ", v.teacher, "/ Turma", v.schoolClass)

