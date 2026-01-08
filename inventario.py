import sqlite3

from colorama import init, Fore, Style



# Inicializa colorama para usar colores en la terminal

init(autoreset=True)



# ------------------- Crear base de datos y tabla -------------------



def crear_base_datos():

    """Crea la base de datos y la tabla 'productos' si no existen."""

    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS productos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            descripcion TEXT,

            cantidad INTEGER NOT NULL,

            precio REAL NOT NULL,

            categoria TEXT

        )

    ''')

    conn.commit()

    conn.close()



# ------------------- Funciones del sistema -------------------



def registrar_producto():

    """Agrega un nuevo producto a la base de datos."""

    print(Fore.GREEN + "\n--- Registrar nuevo producto ---")

    nombre = input("Nombre: ").strip()

    descripcion = input("Descripción: ").strip()

    

    try:

        cantidad = int(input("Cantidad: "))

        precio = float(input("Precio: "))

    except ValueError:

        print(Fore.RED + "Error: La cantidad y el precio deben ser números válidos.")

        return



    categoria = input("Categoría: ").strip()



    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute('''

        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)

        VALUES (?, ?, ?, ?, ?)

    ''', (nombre, descripcion, cantidad, precio, categoria))

    conn.commit()

    conn.close()

    print(Fore.GREEN + "✅ Producto registrado correctamente.")



def visualizar_productos():

    """Muestra todos los productos registrados en la base de datos."""

    print(Fore.CYAN + "\n--- Lista de productos registrados ---")

    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conn.close()



    if productos:

        for prod in productos:

            print(f"ID: {prod[0]}, Nombre: {prod[1]}, Cantidad: {prod[3]}, Precio: ${prod[4]:.2f}, Categoría: {prod[5]}")

    else:

        print(Fore.YELLOW + "⚠️ No hay productos registrados.")



def actualizar_producto():

    """Permite actualizar la información de un producto por su ID."""

    print(Fore.MAGENTA + "\n--- Actualizar producto ---")

    id = input("Ingrese el ID del producto a actualizar: ").strip()

    

    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))

    producto = cursor.fetchone()



    if producto:

        print("Deje vacío el campo si no desea modificarlo.")

        nombre = input(f"Nombre ({producto[1]}): ") or producto[1]

        descripcion = input(f"Descripción ({producto[2]}): ") or producto[2]

        cantidad = input(f"Cantidad ({producto[3]}): ") or producto[3]

        precio = input(f"Precio ({producto[4]}): ") or producto[4]

        categoria = input(f"Categoría ({producto[5]}): ") or producto[5]



        try:

            cantidad = int(cantidad)

            precio = float(precio)

        except ValueError:

            print(Fore.RED + "Error: cantidad o precio inválidos.")

            conn.close()

            return



        cursor.execute('''

            UPDATE productos

            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?

            WHERE id = ?

        ''', (nombre, descripcion, cantidad, precio, categoria, id))

        conn.commit()

        print(Fore.GREEN + "✅ Producto actualizado correctamente.")

    else:

        print(Fore.RED + "❌ Producto no encontrado.")

    

    conn.close()



def eliminar_producto():

    """Elimina un producto de la base de datos por su ID."""

    print(Fore.RED + "\n--- Eliminar producto ---")

    id = input("Ingrese el ID del producto a eliminar: ").strip()

    

    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))

    producto = cursor.fetchone()



    if producto:

        confirmacion = input("¿Está seguro de eliminar este producto? (s/n): ").lower()

        if confirmacion == "s":

            cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

            conn.commit()

            print(Fore.GREEN + "✅ Producto eliminado correctamente.")

        else:

            print(Fore.YELLOW + "❌ Operación cancelada.")

    else:

        print(Fore.RED + "❌ Producto no encontrado.")

    

    conn.close()



def buscar_producto():

    """Permite buscar productos por ID, nombre o categoría."""

    print(Fore.BLUE + "\n--- Buscar producto ---")

    print("Buscar por: [1] ID, [2] Nombre, [3] Categoría")

    opcion = input("Seleccione una opción: ").strip()



    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()



    if opcion == "1":

        id = input("ID: ").strip()

        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))

    elif opcion == "2":

        nombre = input("Nombre: ").strip()

        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))

    elif opcion == "3":

        categoria = input("Categoría: ").strip()

        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", ('%' + categoria + '%',))

    else:

        print(Fore.YELLOW + "❌ Opción inválida.")

        conn.close()

        return



    productos = cursor.fetchall()

    conn.close()



    if productos:

        for prod in productos:

            print(f"ID: {prod[0]}, Nombre: {prod[1]}, Cantidad: {prod[3]}, Precio: ${prod[4]:.2f}, Categoría: {prod[5]}")

    else:

        print(Fore.YELLOW + "⚠️ No se encontraron productos.")



def reporte_bajo_stock():

    """Genera un listado de productos con cantidad menor o igual al límite indicado."""

    print(Fore.YELLOW + "\n--- Reporte de productos con bajo stock ---")

    try:

        limite = int(input("Mostrar productos con cantidad igual o inferior a: "))

    except ValueError:

        print(Fore.RED + "❌ Debe ingresar un número válido.")

        return



    conn = sqlite3.connect('inventario.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))

    productos = cursor.fetchall()

    conn.close()



    if productos:

        print(Fore.LIGHTYELLOW_EX + f"\nProductos con cantidad menor o igual a {limite}:")

        for prod in productos:

            print(f"ID: {prod[0]}, Nombre: {prod[1]}, Cantidad: {prod[3]}")

    else:

        print(Fore.GREEN + "✅ Todos los productos tienen suficiente stock.")



# ------------------- Menú principal -------------------



def menu():

    """Muestra el menú principal e interactúa con el usuario."""

    while True:

        print(Fore.CYAN + Style.BRIGHT + """

========= MENÚ PRINCIPAL =========

1. Registrar nuevo producto

2. Visualizar productos

3. Actualizar producto

4. Eliminar producto

5. Buscar producto

6. Reporte de bajo stock

7. Salir

""")

        opcion = input("Seleccione una opción: ").strip()



        if opcion == "1":

            registrar_producto()

        elif opcion == "2":

            visualizar_productos()

        elif opcion == "3":

            actualizar_producto()

        elif opcion == "4":

            eliminar_producto()

        elif opcion == "5":

            buscar_producto()

        elif opcion == "6":

            reporte_bajo_stock()

        elif opcion == "7":

            print(Fore.GREEN + "👋 ¡Gracias por usar el sistema de inventario!")

            break

        else:

            print(Fore.RED + "❌ Opción inválida. Intente nuevamente.")



# ------------------- Inicio del programa -------------------



if __name__ == "__main__":

    crear_base_datos()  # Crea la base de datos si no existe

    menu()              # Inicia el menú principal

