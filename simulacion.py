from particulaMasa import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from pymongo import MongoClient
import pymongo

class Simulacion(ParticulaMasa):

    def __init__(self, numeroParticulas, tiempoTotal):
        self.numParticulas = numeroParticulas
        self.tiempoTot = tiempoTotal
        self.deltaT = 0.1

        self.particulas = []

        cliente = MongoClient()
        self.db=cliente.ParticulasDB

        for i in range(self.numParticulas):
            self.particulas.append(ParticulaMasa())
            #self.particulas[i].init_random() #Esta instrucción la vamos a cambiar porque ahora no son valores aleatorios como en el
            # ejercicio del Tema 2, sino que tenemos que llamar a set_valores porque los valores los tomaremos de la base de datos 
            #Ahora tenemos que sacar cada uno de los datos de cada partícula
            particula=self.db.Iniciales.find_one({"id":i},{"_id":0})


            pos=np.array(particula["pos"])
            vel=np.array(particula["vel"])
            acc=np.array(particula["acc"])
            masa=particula["masa"]
            
            self.particulas[i].set_valores(pos,vel,acc,masa)

        self.prepara_grafico()


    def avanza(self):
        for i in range(self.numParticulas):
            self.particulas[i].aceleracion_cero()

        for k in range(self.numParticulas):
            for j in range(self.numParticulas):
                if k != j:
                    self.particulas[k].aceleracion_gravitatoria(self.particulas[j])
        
        for l in range (self.numParticulas):
            self.particulas[l].actualiza_velocidad_y_posicion(self.deltaT)
            
        self.refresca_particulas()

    def vectoriza(self):
        x=np.zeros(self.numParticulas)
        y=np.zeros(self.numParticulas)
        z=np.zeros(self.numParticulas)

        for i in range(self.numParticulas):
            x[i] = self.particulas[i].pos[0]
            y[i] = self.particulas[i].pos[1]
            z[i] = self.particulas[i].pos[2]

        return x, y, z

    def simula(self):
        i=0
        while(i<self.tiempoTot):
            self.avanza()
            for k in range(self.numParticulas):
                self.particulas[k].muestra()
                self.db.Valores.insert_one({"id":k, "pos":self.particulas[k].pos.tolist(), "vel":self.particulas[k].vel.tolist(), "acc":self.particulas[k].acc.tolist(), "masa": self.particulas[k].masa, "tiempo":i})
            i+=self.deltaT      

    def prepara_grafico(self):
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.set_xlim(-2.5,2.5)
        self.ax.set_ylim(-2.5,2.5)
        self.ax.set_zlim(-2.5,2.5)
        self.grafico = self.ax.scatter([],[],[],c='r',marker='o')
        
        plt.draw()

    def refresca_particulas(self):
        self.grafico.remove()
        #Limpia el grafico para mostrar las posiciones nuevas
        col=['g']
        # La primera verde y el resto rojas
        for i in range (1,self.numParticulas):
            col.append('r')
        
        x,y,z = self.vectoriza()

        self.grafico = self.ax.scatter(x,y,z,c=col,marker='o')
        plt.draw()
        plt.pause(1)