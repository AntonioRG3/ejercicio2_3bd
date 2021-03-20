from particula import *
G= 6.67259e-11

class ParticulaMasa(Particula):
    def __init__(self):
        super().__init__()
        self.masa = 0

    def set_valores(self, pPos, pVel, pAcc, pMasa):
        """
          Inicializa la posición y la velocidad con los valores dados
        """
        super().set_valores(pPos, pVel, pAcc)
        self.masa = pMasa

    def init_random(self):
        """
          Inicializa la posición y la velocidad de forma aleatoria
        """
        self.set_valores(np.array([random(), random(), random() ]), np.array([random(), random(), random()]),
        np.array( [random(), random(), random()]), random())

    def muestra(self):
        """
          Mustra por Terminal los valores de los atributos
        """  
        super().muestra()
        print("   La masa es: ", self.masa)

    def aceleracion_cero(self):
      self.acc=np.zeros(3)
    
    def aceleracion_gravitatoria(self, otra):
        softening = 1e-6 
        distancia = self.distancia (otra)
        if distancia < softening:
            distancia = softening
        distanciaInv = 1.0 / distancia
        delta = otra.pos - self.pos
        self.acc += delta* G * otra.masa * distanciaInv ** 3