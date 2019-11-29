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
        self.horarioId = None
        self.saturacao = -1


class Escola(object):
    def __init__(self):
        self.vertices = []
        self.listaVerticesId = []
        self.listaCores = []
        self.cores = 0
        self.horario = []
        self.verticeNaoColorido = []
        self.G = nx.Graph()
        self.lerDadosEscolaArquivo()
        self.criarAdjacencias()
        self.colorir()
        self.adicionaCores()
        self.printar()

        # print(df.tail(3))

    def lerDadosEscolaArquivo(self):
        fileXLSX = pd.ExcelFile('./public/files/Escola_A.xlsx')
        df = pd.read_excel(fileXLSX, 'Dados')
        listaArquivo = df.to_numpy()
        verticeId = 0
        for linha in listaArquivo:
            for i in range(int(linha[3])):
                self.listaVerticesId.append(verticeId)
                vertice = Vertice(verticeId, linha[0], linha[1], linha[2])
                self.G.add_node(verticeId)
                self.vertices.append(vertice)
                verticeId += 1

    def criarAdjacencias(self):
        for v1 in self.vertices:
            for v2 in self.vertices:
                if(v1.idVertice != v2.idVertice and (v1.turma == v2.turma or v1.professor == v2.professor)):
                    v1.adjacents.append(v2)
                    v2.adjacents.append(v1)
                    self.G.add_edge(v1.idVertice, v2.idVertice)

    def adicionaCores(self):

        for i in range(len(self.vertices)):
            r = lambda: random.randint(0, 255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            self.listaCores.append(color)

    def printar(self):
        print("Nodes of graph: ")
        print(self.G.nodes())
        print("Edges of graph: ")
        print(self.G.edges())
        print("Quantidade de cor: ")
        print(self.cores)

        for v1 in self.vertices:
            if(v1.horarioId != None) :
                print("Horário: ", self.horario[v1.horarioId], "|| Matéria: ", v1.materia, " || Professor: ", v1.professor, " || Turma: ", v1.turma)
                # print("Matéria: ", v1.materia)
                # print("Professor: ", v1.professor)
                # print("Turma: ", v1.turma)

        nx.draw(self.G, node_color = self.listaCores, with_labels = True)
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
                self.horario.append("{} - {}".format(day, hour))

        self.vertices.sort(key=lambda x: x.saturacao, reverse=True)
        

        while(len(self.listaVerticesId) > 0):
            self.listaVerticesId.sort(reverse=True)
            maxVertice = self.vertices[self.listaVerticesId[0]]
            for index in self.listaVerticesId:
                if(self.vertices[index].saturacao > maxVertice.saturacao or (self.vertices[index].saturacao == maxVertice.saturacao and len(self.vertices[index].adjacents) > len(maxVertice.adjacents))):
                    maxVertice = self.vertices[index]


            colorValidate = False
            while(self.cores < len(self.horario) and not colorValidate):
                colorValidate = True
                for adjacent in maxVertice.adjacents:
                    if(adjacent.horarioId == self.cores ):
                        colorValidate = False
                        self.cores  += 1

            if(self.cores < len(self.horario)):
                for adjacent in maxVertice.adjacents:
                    adjacent.saturacao += 1
                maxVertice.horarioId = self.cores 
            else:
                self.verticeNaoColorido.append(maxVertice.idVertice)

            if maxVertice.idVertice in self.listaVerticesId:
                self.listaVerticesId.remove(maxVertice.idVertice)




       
        # for u in self.vertices:
        #     maxVertice = u

        #     for v in self.vertices:
        #         if(v.saturacao > verticeMaiorSaturacao.saturacao or (v.saturacao == verticeMaiorSaturacao.saturacao and len(v.adjacents) > len(verticeMaiorSaturacao.adjacents))):
        #             verticeMaiorSaturacao = v


        #     colorValidate = False
        #     while(self.cores < len(self.horario) and not colorValidate):
        #         colorValidate = True
        #         for adjacent in verticeMaiorSaturacao.adjacents:
        #             if(adjacent.horarioId == self.cores ):
        #                 colorValidate = False
        #                 self.cores  += 1

        #     if(self.cores < len(self.horario)):
        #         for adjacent in verticeMaiorSaturacao.adjacents:
        #             adjacent.saturacao += 1
        #         verticeMaiorSaturacao.horarioId = self.cores 
        #     else:
        #         self.verticeNaoColorido.append(verticeMaiorSaturacao.idVertice)

            

        


E = Escola()



print("--- %s seconds ---" % (time.time() - start_time))
