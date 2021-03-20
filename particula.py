from random import random, seed
from math import sqrt
import numpy as np

class Particula:
    __cuantas = 0
    def __init__(self):
        self.pos= np.zeros(3)
        self.vel= np.zeros(3)
        self.acc= np.zeros(3)
        self.id = Particula.__cuantas
        Particula.__cuantas += 1
 
    def set_valores(self, pPos, pVel,pAcc):
        """
          Inicializa la posición y la velocidad con los valores dados
        """
        self.pos= pPos   
        self.vel= pVel
        self.acc= pAcc
    
    def init_random(self):
        """
          Inicializa la posición y la velocidad de forma aleatoria
        """
        self.set_valores(np.array([random(), random(), random() ]), np.array([random(), random(), random()]),
        np.array( [random(), random(), random()])),    

    def muestra(self):
        """
          Mustra por Terminal los valores de los atributos
        """  
        print("Partícula ", self.id)
        print("   La posición es: ", self.pos)
        print("   La velocidad es: ", self.vel)
        print("   La acc es: ", self.acc)

    def distancia(self, otra):
        """
          Devuelve la distancia entre dos partículas
        """  
        delta=self.pos - otra.pos
        res = sqrt (delta[0] ** 2 + delta[1] ** 2 + delta[2] **2)
        return res

    @classmethod
    def cuantas(cls):
        return Particula.__cuantas

    def actualiza_velocidad_y_posicion (self, tstep):
        self.vel += self.acc * float(tstep)
        self.pos += self.vel * float(tstep)