from conexion import miConexion, cur

def registrar_producto(nombre, codigo, valor_neto, valor_venta, stock_actual, id_categoria, ubicacion):
    # Assume that you have a table 'UbicacionProducto' where you store locations.
    query_ubicacion = """
        INSERT INTO UbicacionProducto (ubicacion) 
        VALUES (%s) 
        ON DUPLICATE KEY UPDATE idUbicacion=LAST_INSERT_ID(idUbicacion)
    """
    
    # Add the location to the location table (if necessary)
    cur.execute(query_ubicacion, (ubicacion,))
    id_ubicacion = cur.lastrowid  # Get the last inserted or existing location ID
    
    # Insert the new product into the Producto table
    query_producto = """
        INSERT INTO Producto (nombre, codigo, valor_neto, valor_venta, stock_actual, idCategoria, Ubicacion_idUbicacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cur.execute(query_producto, (nombre, codigo, valor_neto, valor_venta, stock_actual, id_categoria, id_ubicacion))
    miConexion.commit()
    print("Producto registrado exitosamente.")


def actualizar_producto(id_producto, nombre=None, codigo=None, stock_actual=None, id_categoria=None):
    updates = []
    values = []
    if nombre:
        updates.append("nombre = %s")
        values.append(nombre)
    if codigo:
        updates.append("codigo = %s")
        values.append(codigo)
    if stock_actual is not None:  # Verificamos si el stock es proporcionado
        updates.append("stock_actual = %s")
        values.append(stock_actual)
    if id_categoria:
        updates.append("idCategoria = %s")
        values.append(id_categoria)

    values.append(id_producto)
    query = f"UPDATE Producto SET {', '.join(updates)} WHERE idProducto = %s"
    cur.execute(query, values)
    miConexion.commit()
    print("Producto actualizado exitosamente.")

def consultar_producto(id_producto):
    query = """
    SELECT p.idProducto, p.nombre, p.codigo, p.stock_actual, c.nombre
    FROM Producto AS p
    LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria
    WHERE p.idProducto = %s
    """
    cur.execute(query, (id_producto,))
    producto = cur.fetchone()
    
    if producto:
        print("Información del producto:")
        print("ID Producto:", producto[0])
        print("Nombre:", producto[1])
        print("Código:", producto[2])
        print("Stock Actual:", producto[3])
        print("Categoría:", producto[4] if producto[4] else "Sin categoría")
    else:
        print("Producto no encontrado.")

def eliminar_producto(codigo):
    # Verificar que el producto con el código especificado exista en la base de datos
    cur.execute("SELECT idProducto FROM Producto WHERE codigo = %s", (codigo,))
    resultado = cur.fetchone()

    if resultado is None:
        print("Producto no encontrado con el código especificado.")
        return

    # Eliminar el producto de la tabla Producto usando su código
    cur.execute("DELETE FROM Producto WHERE codigo = %s", (codigo,))
    miConexion.commit()
    print("Producto eliminado exitosamente.")

