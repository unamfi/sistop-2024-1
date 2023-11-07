import threading

# Inventario inicial como un diccionario vacío
inventario = {}

# Objeto Condition para controlar el acceso concurrente al inventario
condition = threading.Condition()

def agregar_producto():
    producto = input("Introduce el nombre del producto a agregar: ")
    with condition:
        if producto in inventario:
            print("El producto ya existe.")
        else:
            inventario[producto] = 0
            condition.notify_all()
    mostrar_inventario()

def modificar_stock():
    producto = input("Introduce el nombre del producto a modificar: ")
    cantidad = int(input("Introduce la cantidad a modificar (negativo para despachar): "))
    with condition:
        if producto in inventario and (inventario[producto] + cantidad) >= 0:
            inventario[producto] += cantidad
            condition.notify_all()
        else:
            print("Stock insuficiente o el producto no existe.")
    mostrar_inventario()

def mostrar_inventario():
    print("Inventario actualizado:")
    for producto, cantidad in inventario.items():
        print(f"{producto}: {cantidad}")

def menu():
    while True:
        print("\n-- Manejador de Inventario --")
        print("1. Agregar producto nuevo")
        print("2. Modificar stock de un producto")
        print("3. Mostrar inventario")
        print("4. Salir")
        opcion = input("Introduce una opción: ")
        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            modificar_stock()
        elif opcion == '3':
            mostrar_inventario()
        elif opcion == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

# Inicio del programa
if __name__ == "__main__":
    menu()
