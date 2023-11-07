import threading

class Metro:
    def __init__(self):
        self.pasajeros_dentro = 0
        self.puertas_abiertas = False
        self.pasajeros_bajando = 0
        self.pasajeros_subiendo = 0
        self.pasajeros_esperando = 0
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)

    def abrir_puertas(self):
        with self.mutex:
            self.puertas_abiertas = True
            self.cond.notify_all()

    def cerrar_puertas(self):
        with self.mutex:
            while self.pasajeros_bajando > 0 or self.pasajeros_subiendo > 0:
                self.cond.wait()
            self.puertas_abiertas = False
            self.cond.notify_all()

    def bajar_pasajero(self):
        with self.mutex:
            while not self.puertas_abiertas or self.pasajeros_subiendo > 0:
                self.cond.wait()
            self.pasajeros_bajando += 1

    def subir_pasajero(self):
        with self.mutex:
            while not self.puertas_abiertas or self.pasajeros_bajando > 0:
                self.cond.wait()
            self.pasajeros_subiendo += 1

    def terminar_bajar(self):
        with self.mutex:
            self.pasajeros_dentro -= 1
            self.pasajeros_bajando -= 1
            self.cond.notify_all()

    def terminar_subir(self):
        with self.mutex:
            self.pasajeros_dentro += 1
            self.pasajeros_subiendo -= 1
            self.cond.notify_all()

    def agregar_pasajero_esperando(self):
        with self.mutex:
            self.pasajeros_esperando += 1

    def quitar_pasajero_esperando(self):
        with self.mutex:
            self.pasajeros_esperando -= 1

    def get_estado_puertas(self):
        with self.mutex:
            return self.puertas_abiertas

    def get_pasajeros_dentro(self):
        with self.mutex:
            return self.pasajeros_dentro

    def get_pasajeros_esperando(self):
        with self.mutex:
            return self.pasajeros_esperando
