def mostrar_menu_principal() -> None:
    print("\n" + "=" * 45)
    print("      INVENTARIO MULTI-PILA - FERRETERÍA FEEL")
    print("=" * 45)
    print("1. Registrar producto en una categoría")
    print("2. Despachar producto reciente")
    print("3. Consultar la cima de una categoría")
    print("4. Mostrar inventario completo")
    print("5. Buscar producto en almacén")
    print("6. Salir")
    print("=" * 45)


def seleccionar_categoria(categorias: dict) -> str | None:
    if not categorias:
        print("No hay categorías disponibles.")
        return None

    print("\n--- Seleccione una Categoría ---")
    llaves = list(categorias.keys())
    for idx, cat in enumerate(llaves, 1):
        print(f"{idx}. {cat}")
    print("0. Cancelar")

    while True:
        opc = input("Ingrese el número de categoría: ").strip()
        if opc == "0":
            return None
        if opc.isdigit() and 1 <= int(opc) <= len(llaves):
            return llaves[int(opc) - 1]
        print("Error: Ingrese un número de opción válido.")


def agregar_producto(categorias: dict) -> None:
    categoria = seleccionar_categoria(categorias)
    if categoria is None:
        return

    # 1. Validación del Nombre (Solo texto/números válidos, descarta únicamente símbolos o espacios)
    while True:
        nombre = input(f"Ingrese el nombre del producto para [{categoria}] (o '0' para cancelar): ").strip().title()
        if nombre == "0":
            print("Operación cancelada.")
            return
        
        # Debe tener al menos una letra o número y no estar vacío
        if nombre and any(c.isalnum() for c in nombre):
            break
        print("Error: El nombre debe contener texto válido (no solo espacios o símbolos).")

    # 2. Validación de Cantidad (Estrictamente enteros positivos > 0, rechaza <= 0 y -0)
    while True:
        entrada_cant = input("Ingrese la cantidad inicial: ").strip()
        try:
            cantidad = int(entrada_cant)
            if cantidad > 0:
                break
            print("Error: La cantidad debe ser un entero positivo mayor a 0 (no se permiten ceros ni negativos).")
        except ValueError:
            print("Error: Ingrese un número entero válido (sin letras, decimales o símbolos).")

    # 3. Validación de Precio (Estrictamente flotantes/enteros positivos > 0, rechaza <= 0 y -0)
    while True:
        entrada_precio = input("Ingrese el precio unitario (C$): ").strip()
        try:
            precio = float(entrada_precio)
            if precio > 0:
                break
            print("Error: El precio debe ser un valor numérico mayor a 0 (no se permiten ceros ni negativos).")
        except ValueError:
            print("Error: Ingrese un precio numérico válido.")

    nuevo_item = {
        "producto": nombre,
        "cantidad": cantidad,
        "precio": precio
    }

    categorias[categoria].append(nuevo_item)
    print(f"\n¡Éxito! Producto '{nombre}' (x{cantidad}) agregado a la pila de {categoria}.")


def despachar_producto(categorias: dict) -> None:
    categoria = seleccionar_categoria(categorias)
    if categoria is None:
        return

    pila = categorias[categoria]
    if not pila:
        print(f"La pila de {categoria} está vacía. No hay elementos para despachar.")
        return

    item_cima = pila[-1]
    print(f"\nProducto en cima a despachar: {item_cima['producto']} (Disponible: {item_cima['cantidad']})")

    # Validación de Cantidad a Despachar (Rechaza negativos, 0 y cantidades mayores al stock)
    while True:
        entrada_desp = input("Ingrese la cantidad a despachar (o '0' para cancelar): ").strip()
        if entrada_desp == "0":
            print("Despacho cancelado.")
            return

        try:
            a_despachar = int(entrada_desp)
            if a_despachar <= 0:
                print("Error: La cantidad a despachar debe ser un número entero positivo (no se permiten ceros ni negativos).")
                continue
            if a_despachar > item_cima['cantidad']:
                print(f"Error: No puede despachar más de la cantidad disponible ({item_cima['cantidad']}).")
                continue
            break
        except ValueError:
            print("Error: Ingrese un número entero válido.")

    item_cima['cantidad'] -= a_despachar
    print(f"¡Se han despachado {a_despachar} unidad(es) de '{item_cima['producto']}'!")

    if item_cima['cantidad'] == 0:
        pila.pop()
        print(f"El producto '{item_cima['producto']}' se ha agotado y fue removido de la cima de la pila.")


def mostrar_cima(categorias: dict) -> None:
    categoria = seleccionar_categoria(categorias)
    if categoria is None:
        return

    pila = categorias[categoria]
    if not pila:
        print(f"La pila de {categoria} está vacía.")
        return

    cima = pila[-1]
    print(f"\n--- CIMA DE LA PILA [{categoria}] ---")
    print(f"Producto: {cima['producto']}")
    print(f"Cantidad: {cima['cantidad']} unidades")
    print(f"Precio:   C$ {cima['precio']:.2f}")


def mostrar_inventario_completo(categorias: dict) -> None:
    print("\n" + "=" * 60)
    print("       INVENTARIO GENERAL DE FERRETERÍA FEEL")
    print("=" * 60)

    for categoria, pila in categorias.items():
        print(f"\n--- Categoría: {categoria} ({len(pila)} lotes de productos) ---")
        if not pila:
            print("  (Pila vacía)")
        else:
            for i, item in enumerate(reversed(pila), 1):
                subtotal = item['cantidad'] * item['precio']
                print(f"  {i}. {item['producto']} | Cant: {item['cantidad']} | Precio Unit: C${item['precio']:.2f} | Total: C${subtotal:.2f}")


def buscar_producto(categorias: dict) -> None:
    termino = input("\nIngrese el nombre del producto a buscar: ").strip().lower()

    # Validación 1: Evitar búsquedas vacías
    if not termino:
        print("Error: El texto de búsqueda no puede estar vacío.")
        return

    # Validación 2: Rechazar si el término es un número negativo o cero (ej: -0, -5, 0)
    try:
        val_num = float(termino)
        if val_num <= 0:
            print("Error: No se permiten términos de búsqueda con números menores o iguales a 0.")
            return
    except ValueError:
        pass  # Es texto normal (no un número), continúa la búsqueda

    encontrados = 0
    print("\n" + "=" * 60)
    print(f"          RESULTADOS DE BÚSQUEDA PARA: '{termino.upper()}'")
    print("=" * 60)

    for categoria, pila in categorias.items():
        for pos_desde_cima, item in enumerate(reversed(pila), 1):
            if termino in item['producto'].lower():
                encontrados += 1
                subtotal = item['cantidad'] * item['precio']
                print(f"► Encontrado en Categoría: [{categoria}]")
                print(f"  Posición en Pila: {pos_desde_cima} (desde la Cima)")
                print(f"  Producto:         {item['producto']}")
                print(f"  Stock Disponible: {item['cantidad']} unidades")
                print(f"  Precio Unitario:  C$ {item['precio']:.2f}")
                print(f"  Valor Total Lote: C$ {subtotal:.2f}")
                print("-" * 60)

    if encontrados == 0:
        print(f"No se encontró ningún producto que coincida con '{termino}'.")


def main():
    inventario_feel = {
        "Obra Gris": [
            {"producto": "Bolsa De Cemento Holcim 42.5kg", "cantidad": 50, "precio": 380.00},
            {"producto": "Varilla De Hierro 3/8\"", "cantidad": 100, "precio": 145.00},
            {"producto": "Bloque De Concreto 15x20x40", "cantidad": 200, "precio": 18.50}
        ],
        "Pinturas": [
            {"producto": "Pintura Aceite Blanco Galón", "cantidad": 15, "precio": 520.00},
            {"producto": "Brocha De Cerda 3\"", "cantidad": 30, "precio": 85.00},
            {"producto": "Pintura Latex Azul Cubeta", "cantidad": 8, "precio": 2100.00}
        ],
        "Herramientas": [
            {"producto": "Martillo De Uña 16oz", "cantidad": 12, "precio": 220.00},
            {"producto": "Alicate Universal 8\"", "cantidad": 20, "precio": 180.00},
            {"producto": "Taladro Percutor 1/2\"", "cantidad": 5, "precio": 1650.00}
        ],
        "PVC": [
            {"producto": "Tubo PVC Presión 1/2\"", "cantidad": 40, "precio": 110.00},
            {"producto": "Codo PVC 90 Grados 1/2\"", "cantidad": 80, "precio": 12.00},
            {"producto": "Pegamento PVC 4oz", "cantidad": 25, "precio": 95.00}
        ]
    }

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            agregar_producto(inventario_feel)
        elif opcion == "2":
            despachar_producto(inventario_feel)
        elif opcion == "3":
            mostrar_cima(inventario_feel)
        elif opcion == "4":
            mostrar_inventario_completo(inventario_feel)
        elif opcion == "5":
            buscar_producto(inventario_feel)
        elif opcion == "6":
            print("Saliendo del sistema de inventario FEEL...")
            break
        else:
            print("Opción no válida. Seleccione un número del 1 al 6.")


if __name__ == "__main__":
    main()