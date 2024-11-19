from conexion import miConexion, cur

def registrar_venta(cliente_id, usuario_id, descuento, detalles):
    """
    Registra una nueva venta en la base de datos.
    detalles: lista de tuplas (producto_id, cantidad, precio_unitario).
    """
    try:
        subtotal = sum(cantidad * precio_unitario for _, cantidad, precio_unitario in detalles)
        igv = subtotal * 0.18
        total = subtotal + igv - descuento

        query_venta = """
            INSERT INTO Venta (fecha, Cliente_idCliente, Usuario_idUsuario, descuento, importe_total, importe_total_igv)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """
        cur.execute(query_venta, (cliente_id, usuario_id, descuento, total, igv))
        venta_id = cur.lastrowid

        query_detalle = """
            INSERT INTO detalle_venta (Venta_idVenta, Producto_idProducto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        for producto_id, cantidad, precio_unitario in detalles:
            cur.execute(query_detalle, (venta_id, producto_id, cantidad, precio_unitario))
        
        miConexion.commit()
        print("Venta registrada exitosamente.")
        return venta_id
    except Exception as e:
        miConexion.rollback()
        print(f"Error al registrar la venta: {e}")

def consultar_venta(venta_id):
    """
    Consulta los detalles de una venta específica.
    """
    try:
        query_venta = """
            SELECT v.idVenta, c.persona, u.nombre, u.apellido, v.fecha, v.descuento, v.importe_total, v.importe_total_igv
            FROM Venta AS v
            JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
            JOIN usuarios AS u ON v.Usuario_idUsuario = u.id_usuario
            WHERE v.idVenta = %s
        """
        cur.execute(query_venta, (venta_id,))
        venta = cur.fetchone()

        query_detalles = """
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.cantidad * dv.precio_unitario AS subtotal
            FROM detalle_venta AS dv
            JOIN Producto AS p ON dv.Producto_idProducto = p.idProducto
            WHERE dv.Venta_idVenta = %s
        """
        cur.execute(query_detalles, (venta_id,))
        detalles = cur.fetchall()

        return venta, detalles
    except Exception as e:
        print(f"Error al consultar la venta: {e}")
        return None, []

def eliminar_venta(venta_id):
    """
    Elimina una venta y sus detalles relacionados.
    """
    try:
        cur.execute("DELETE FROM detalle_venta WHERE Venta_idVenta = %s", (venta_id,))
        cur.execute("DELETE FROM Venta WHERE idVenta = %s", (venta_id,))
        miConexion.commit()
        print("Venta eliminada exitosamente.")
    except Exception as e:
        miConexion.rollback()
        print(f"Error al eliminar la venta: {e}")
