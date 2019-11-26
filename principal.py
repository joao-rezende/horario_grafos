from openpyxl import load_workbook
import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd
import random
start_time = time.time()

class Vertice(object):
    def __init__(self, idVertice, materia, turma, professor):
        self.idVertice = idVertice
        self.materia = materia
        self.turma = turma
        self.professor = professor
        self.adjacents = []
        self.idTarefa = -1
        self.saturacao = 0



class Escola(object):
    def __init__(self):
        self.professores = {}
        self.materias = {}
        self.turmas = {}
        self.horariosResult = []
        self.cores = 0
        self.tarefas = []
        self.G = nx.Graph()
        self.lerDadosEscolaArquivo()
        # print(self.professores)
        self.criarAdjacencias()
        self.colorir()
        self.printar()

        
        # print(df.tail(3))

    


    def lerDadosEscolaArquivo(self):
        fileXLSX = pd.ExcelFile('./public/files/Escola_A.xlsx')
        df = pd.read_excel(fileXLSX, 'Dados')
        listaArquivo = df.to_numpy()
        verticeId = 0
        for linha in listaArquivo:
            for i in range(int(linha[3])):
                vertice = Vertice(verticeId, linha[0], linha[1], linha[2])
                self.G.add_node(verticeId)
                self.horariosResult.append('gray')
                self.professores[verticeId] = vertice
                verticeId += 1

    def criarAdjacencias(self):
        for v1 in self.professores.values():
            for v2 in self.professores.values():
                if(v1.idVertice != v2.idVertice and (v1.materia == v2.materia or v1.professor == v2.professor)):
                    v1.adjacents.append(v2)
                    v2.adjacents.append(v1)
                    self.G.add_edge(v1.idVertice, v2.idVertice)
                    self.G[v1.idVertice][v2.idVertice]['color']='red'


    def printar(self):
        print("Nodes of graph: ")
        print(self.G.nodes())
        print("Edges of graph: ")
        print(self.G.edges())
        

        for v1 in self.professores.values():
            # print(v)
            if(v1.idTarefa != None) :
                print("Horário: ", self.tarefas[v1.idTarefa], "|| Matéria: ", v1.materia, " || Professor: ", v1.professor, " || Turma: ", v1.turma)
                # print("Matéria: ", v1.materia)
                # print("Professor: ", v1.professor)
                # print("Turma: ", v1.turma)


        nx.draw(self.G, node_color = self.horariosResult, with_labels = True)
        plt.savefig("simple_path.png") # save as png
        plt.show() # display


    def colorir(self):
        days_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        hours = []

        fileXLSX = pd.ExcelFile('./public/files/Escola_A.xlsx')
        df = pd.read_excel(fileXLSX, 'Configuracoes')
        listaArquivo = df.to_numpy()        


        for line in listaArquivo:
            hours.append(line[0])

        for day in days_week:
            for hour in hours:
                self.tarefas.append("{} - {}".format(day, hour))

        notColoring = []
       
        verticeMaiorSaturacao = self.professores[1]
        for v1 in self.professores.values():
            if(v1.saturacao > verticeMaiorSaturacao.saturacao or (v1.saturacao == verticeMaiorSaturacao.saturacao
                and len(v1.adjacents) > len(verticeMaiorSaturacao.adjacents))):
                verticeMaiorSaturacao = v1


            colorValidate = False
            while(self.cores < len(self.tarefas) and not colorValidate):
                colorValidate = True
                for adjacent in verticeMaiorSaturacao.adjacents:
                    if(adjacent.idTarefa == self.cores ):
                        colorValidate = False
                        self.cores  += 1

            if(self.cores < len(self.tarefas)):
                for adjacent in verticeMaiorSaturacao.adjacents:
                    adjacent.saturacao += 1
                verticeMaiorSaturacao.idTarefa = self.cores 
            else:
                notColoring.append(verticeMaiorSaturacao.idVertice)

        


E = Escola()



print("--- %s seconds ---" % (time.time() - start_time))