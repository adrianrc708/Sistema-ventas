from conexion import miConexion, cur

def ventas_por_cliente(cliente_nombre):
    query = """
    SELECT 
        Venta.idVenta, 
        Venta.fecha, 
        Producto.nombre, 
        detalle_venta.cantidad
    FROM Venta
    LEFT JOIN detalle_venta ON Venta.idVenta = detalle_venta.Venta_idVenta
    LEFT JOIN Producto ON detalle_venta.Producto_idProducto = Producto.idProducto
    LEFT JOIN Cliente ON Venta.Cliente_idCliente = Cliente.idCliente
    WHERE Cliente.persona LIKE %s
    ORDER BY Venta.fecha DESC;
    """
    cur.execute(query, ('%' + cliente_nombre + '%',))
    ventas_cliente = cur.fetchall()
    
    return ventas_cliente


def reporte_ventas():
    query = """
    SELECT Cliente.persona, COUNT(DISTINCT Venta.idVenta) AS numero_compras
    FROM Venta
    JOIN Cliente ON Venta.Cliente_idCliente = Cliente.idCliente
    GROUP BY Cliente.idCliente
    HAVING COUNT(DISTINCT Venta.idVenta) > 3
    ORDER BY numero_compras DESC
    """
    cur.execute(query)
    ventas = cur.fetchall()
    
    return ventas
    
def reporte_inventario():
    query = """
    SELECT Producto.nombre, Producto.stock_actual
    FROM Producto
    WHERE Producto.stock_actual < 4
    ORDER BY Producto.stock_actual ASC
    """
    cur.execute(query)
    inventario = cur.fetchall()
    
    return inventario
