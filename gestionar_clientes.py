from conexion import miConexion, cur

def registrar_cliente(persona, direccion, telefono, dni_ruc):
    query = "INSERT INTO Cliente (persona, direccion, telefono, DNI_RUC) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (persona, direccion, telefono, dni_ruc))
    miConexion.commit()
    print("Cliente registrado exitosamente.")

def actualizar_cliente(dni_ruc, persona=None, direccion=None, telefono=None):
    updates = []
    values = []
    if persona:
        updates.append("persona = %s")
        values.append(persona)
    if direccion:
        updates.append("direccion = %s")
        values.append(direccion)
    if telefono:
        updates.append("telefono = %s")
        values.append(telefono)

    values.append(dni_ruc)
    query = f"UPDATE Cliente SET {', '.join(updates)} WHERE DNI_RUC = %s"
    cur.execute(query, values)
    miConexion.commit()
    print("Cliente actualizado exitosamente.")

def consultar_cliente(dni_ruc):
    query = "SELECT * FROM Cliente WHERE DNI_RUC = %s"
    cur.execute(query, (dni_ruc,))
    cliente = cur.fetchone()
    
    if cliente:
        print("Información del cliente:")
        print("Nombre:", cliente[1])
        print("Dirección:", cliente[2])
        print("Teléfono:", cliente[3])
        print("DNI/RUC:", cliente[4])
    else:
        print("Cliente no encontrado.")

    query = """
    SELECT Venta.idVenta, Venta.fecha, detalle_venta.cantidad, detalle_venta.precio_unitario * detalle_venta.cantidad AS monto_total
    FROM Venta
    JOIN detalle_venta ON Venta.idVenta = detalle_venta.Venta_idVenta
    JOIN Cliente ON Venta.Cliente_idCliente = Cliente.idCliente
    WHERE Cliente.DNI_RUC = %s
    """
    cur.execute(query, (dni_ruc,))
    compras = cur.fetchall()
    
    if compras:
        print("\nHistorial de compras:")
        for compra in compras:
            print(f"ID Venta: {compra[0]}, Fecha: {compra[1]}, Cantidad: {compra[2]}, Monto Total: {compra[3]:.2f}")
    else:
        print("No hay historial de compras para este cliente.")

def eliminar_cliente(id_cliente):
    # Verificar que el cliente con el ID especificado exista en la base de datos
    cur.execute("SELECT idCliente FROM Cliente WHERE idCliente = %s", (id_cliente,))
    resultado = cur.fetchone()

    if resultado is None:
        print("Cliente no encontrado con el ID especificado.")
        return

    # Proceder a eliminar registros en las tablas relacionadas
    # Eliminar registros de detalle_venta asociados al cliente
    cur.execute("""
        DELETE FROM detalle_venta
        WHERE Venta_idVenta IN (SELECT idVenta FROM Venta WHERE Cliente_idCliente = %s)
    """, (id_cliente,))
    
    # Eliminar registros de Venta asociados al cliente
    cur.execute("DELETE FROM Venta WHERE Cliente_idCliente = %s", (id_cliente,))
    
    # Eliminar el cliente de la tabla Cliente
    cur.execute("DELETE FROM Cliente WHERE idCliente = %s", (id_cliente,))
    miConexion.commit()
    print("Cliente y registros asociados eliminados exitosamente.")





    #----------------------------------------------------

    