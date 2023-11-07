import threading
import random
import tkinter as tk

class ProbadorRopa:
    def __init__(self):
        self.mutex = threading.Lock()# permite que solo un hilo acceda a un recurso compartido a la vez
        self.probadores_disponibles = [1, 2, 3]

  
#La persona quiere entrar a un probador entonces verifica si hay probadores disponibles.
#si no hay probadores disponibles, la persona espera hasta que haya uno disponible si hay un probador disponible, la persona entra al probador y comienza a probarse la ropa.
#después de probarse la ropa, la persona sale del probador.El probador que la persona utilizó se marca como disponible para que otra persona pueda usarlo.     
    def entrar(self, persona):
        with self.mutex:
            while not self.probadores_disponibles:
                self.mutex.release()#libera el bloqueo 
                self.mutex.acquire()#lo bloquea 

            probador = self.probadores_disponibles.pop(0)

        print(f"{persona} ha entrado al probador {probador}")

        num_prendas = random.randint(0, 5)
        for prendas_probadas in range(num_prendas):
            print(f"{persona} está probando la prenda {prendas_probadas + 1} en el probador {probador}")

        self.salir(persona, probador)
# marca el probador como disponible una vez que la persona ha terminado de usarlo. 
# permitiendo  que otras personas puedan usar el probador
    def salir(self, persona, probador):
        with self.mutex:
            self.probadores_disponibles.append(probador)

        print(f"{persona} ha salido del probador")
# inicia con varias personas probándose ropa 
# para que empiecen a probarse la ropa al mismo tiempo en cada probador
def iniciar_programa():
    probador = ProbadorRopa()

    personas = ["Persona 1", "Persona 2", "Persona 3", "Persona 4", "Persona 5"]

    threads = []
    for persona in personas:
        t = threading.Thread(target=probador.entrar, args=(persona,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Boutique FI")
    ventana.geometry("1000x500")
    ventana.configure(bg="pink")

    etiquetas = []
    for i in range(3):
        for j in range(3):
            etiqueta = tk.Label(ventana, text=f"Probador {i*3+j+1}: Libre", bg="pink", font=("Arial", 12), relief="solid")
            etiqueta.grid(row=i, column=j, padx=50, pady=60)
            etiquetas.append(etiqueta)

    boton_inicio = tk.Button(ventana, text="Iniciar Programa", command=iniciar_programa)
    boton_inicio.grid(row=5, column=0, columnspan=7, pady=20)

    ventana.mainloop()

crear_interfaz()
