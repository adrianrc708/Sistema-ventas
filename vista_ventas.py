import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from gestionar_ventas import registrar_venta, consultar_venta, eliminar_venta
from conexion import cur
import tkinter.ttk as ttk
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter.simpledialog as simpledialog

class CRUDventas:
    def crud(self):
        from main import MainApp

        def cargar_ventas():
            """Carga las ventas en la tabla de la interfaz."""
            global table  # Aseguramos que table esté definido correctamente

            # Validar si el widget `table` existe antes de intentar usarlo
            try:
                for item in table.get_children():
                    table.delete(item)
            except NameError:
                messagebox.showerror("Error", "La tabla no está inicializada. Asegúrate de haber llamado a mostrar_crud primero.")
                return

            try:
                # Consulta a la base de datos
                cur.execute("""
                    SELECT v.idVenta, c.persona, CONCAT(u.nombre, ' ', u.apellido) AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.idUsuario = u.id_usuario;
                """)
                ventas = cur.fetchall()

                # Insertar datos en la tabla
                for venta in ventas:
                    table.insert("", "end", values=venta)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar las ventas: {e}")


        # Mantén todas las funciones relacionadas globales accesibles y evita destruir widgets innecesariamente

        def mostrar_crud():
            """Reconstruye la interfaz principal para mostrar la tabla de ventas."""
            global table, detalles_table, id_entry, cliente_entry, trabajador_entry  # Aseguramos que las variables sean globales y estén disponibles

            # Limpiar el contenido actual del frame
            for widget in frame_light_gray.winfo_children():
                widget.destroy()

            # Crear el título de la sección
            title_label = ctk.CTkLabel(frame_light_gray, text="GESTIÓN DE VENTAS", font=("Comic Sans MS", 30, "bold"))
            title_label.pack(pady=20)

            # Crear el frame de búsqueda y botones
            search_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
            search_frame.pack(pady=10)

            # Buscar por ID
            id_label = ctk.CTkLabel(search_frame, text="ID Venta:", font=("Comic Sans MS", 14))
            id_label.grid(row=0, column=0, padx=5, pady=5)

            id_entry = ctk.CTkEntry(search_frame, width=100)
            id_entry.grid(row=0, column=1, padx=5, pady=5)

            search_button = ctk.CTkButton(search_frame, text="Buscar ID", command=buscar_venta, width=80, fg_color=custom_color, hover_color="#B03B4A")
            search_button.grid(row=0, column=2, padx=10, pady=5)

            # Buscar por Cliente
            cliente_label = ctk.CTkLabel(search_frame, text="Cliente:", font=("Comic Sans MS", 14))
            cliente_label.grid(row=1, column=0, padx=5, pady=5)

            cliente_entry = ctk.CTkEntry(search_frame, width=100)
            cliente_entry.grid(row=1, column=1, padx=5, pady=5)

            cliente_search_button = ctk.CTkButton(search_frame, text="Buscar Cliente", command=buscar_venta_por_cliente, width=100, fg_color=custom_color, hover_color="#B03B4A")
            cliente_search_button.grid(row=1, column=2, padx=10, pady=5)

            # Buscar por Trabajador
            trabajador_label = ctk.CTkLabel(search_frame, text="Trabajador:", font=("Comic Sans MS", 14))
            trabajador_label.grid(row=2, column=0, padx=5, pady=5)

            trabajador_entry = ctk.CTkEntry(search_frame, width=100)
            trabajador_entry.grid(row=2, column=1, padx=5, pady=5)

            trabajador_search_button = ctk.CTkButton(search_frame, text="Buscar Trabajador", command=buscar_venta_por_trabajador, width=120, fg_color=custom_color, hover_color="#B03B4A")
            trabajador_search_button.grid(row=2, column=2, padx=10, pady=5)

            delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_venta_id, width=80, fg_color=custom_color, hover_color="#B03B4A")
            delete_button.grid(row=0, column=3, padx=10, pady=5)

            print_button = ctk.CTkButton(search_frame, text="Imprimir", command=imprimir_factura, width=80, fg_color=custom_color, hover_color="#B03B4A")
            print_button.grid(row=0, column=4, padx=10, pady=5)

            # Crear el frame para la tabla de ventas
            table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white")
            table_frame.pack(pady=20, fill="x", padx=20)

            # Configurar las columnas de la tabla de ventas
            columns = ("ID Venta", "Cliente", "Usuario", "Fecha", "Total")
            table = ttk.Treeview(table_frame, columns=columns, show="headings")
            table.pack(fill="both", expand=True)

            # Estilo de la tabla de ventas
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"), background=custom_color, foreground="black")
            style.configure("Treeview", rowheight=20, background="white", foreground="black", bordercolor="black", borderwidth=1)
            style.map("Treeview", background=[("selected", "#D04A5D")])

            # Definir los anchors específicos para cada columna
            table.heading("ID Venta", text="ID Venta")
            table.column("ID Venta", anchor="center", width=100)

            table.heading("Cliente", text="Cliente")
            table.column("Cliente", anchor="center", width=150)

            table.heading("Usuario", text="Usuario")
            table.column("Usuario", anchor="center", width=150)

            table.heading("Fecha", text="Fecha")
            table.column("Fecha", anchor="center", width=120)

            table.heading("Total", text="Total")
            table.column("Total", anchor="center", width=100)

            # Crear el frame para la tabla de detalles de la venta
            detalles_frame = ctk.CTkFrame(frame_light_gray, fg_color="white")
            detalles_frame.pack(pady=10, fill="x", padx=20)

            # Configurar las columnas de la tabla de detalles
            detalles_columns = ("ID Detalle Venta", "ID Producto", "Producto", "Precio Unitario", "Cantidad")
            detalles_table = ttk.Treeview(detalles_frame, columns=detalles_columns, show="headings")
            detalles_table.pack(fill="both", expand=True)

            # Estilo de la tabla de detalles
            for col in detalles_columns:
                detalles_table.heading(col, text=col)
                detalles_table.column(col, anchor="center")

            # Definir los anchors específicos para cada columna en la tabla de detalles
            detalles_table.column("ID Detalle Venta", anchor="center", width=100)
            detalles_table.column("ID Producto", anchor="center", width=100)
            detalles_table.column("Producto", anchor="center", width=200)
            detalles_table.column("Precio Unitario", anchor="center", width=120)
            detalles_table.column("Cantidad", anchor="center", width=100)

            # Cargar las ventas en la tabla
            cargar_ventas()


        def imprimir_factura():
            """Imprime la factura de la venta seleccionada en la tabla de ventas."""
            global table  # Asegúrate de que table esté accesible globalmente
    
            # Verificar si la tabla existe
            if not table:
                messagebox.showerror("Error", "La tabla de ventas no está disponible.")
                return

            selected_item = table.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione una venta para imprimir.")
                return

            venta_id = table.item(selected_item, "values")[0]
    
            try:
                # Llamar a la función para generar la factura
                generar_factura_automatica(venta_id)
                messagebox.showinfo("Éxito", f"Factura de la venta {venta_id} generada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la factura: {e}")            




        def buscar_venta():
            """Busca una venta por ID y muestra sus detalles en la tabla de detalles."""
            global id_entry, table, detalles_table

            venta_id = id_entry.get().strip()
            if not venta_id or not venta_id.isdigit():
                messagebox.showwarning("Advertencia", "Ingrese un ID de venta válido.")
                return

            for item in table.get_children():
                table.delete(item)

            for detalle in detalles_table.get_children():
                detalles_table.delete(detalle)

            try:
                # Consulta la venta en la base de datos
                cur.execute("""
                    SELECT v.idVenta, c.persona, CONCAT(u.nombre, ' ', u.apellido) AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.idUsuario = u.id_usuario
                    WHERE v.idVenta = %s;
                """, (venta_id,))
                venta = cur.fetchone()

                if venta:
                    # Inserta la venta encontrada en la tabla de ventas
                    table.insert("", "end", values=venta)

                    # Consulta los detalles de la venta, incluyendo el nombre del producto
                    cur.execute("""
                        SELECT dv.iddetalle_venta, dv.Producto_idProducto, p.nombre AS nombre_producto, 
                            dv.precio_unitario, dv.cantidad
                        FROM detalle_venta AS dv
                        JOIN Producto AS p ON dv.Producto_idProducto = p.idProducto
                        WHERE dv.Venta_idVenta = %s;
                    """, (venta_id,))
                    detalles = cur.fetchall()

                    # Inserta los detalles en la tabla de detalles
                    for detalle in detalles:
                        detalles_table.insert("", "end", values=detalle)
                else:
                    messagebox.showinfo("Resultado", "No se encontró la venta.")

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar la venta: {e}")
                
        def buscar_venta_por_cliente():
            """Busca ventas por cliente y muestra los resultados en la tabla."""
            global cliente_entry, table, detalles_table

            cliente = cliente_entry.get().strip()
            if not cliente:
                messagebox.showwarning("Advertencia", "Ingrese un nombre de cliente válido.")
                return

            for item in table.get_children():
                table.delete(item)

            for detalle in detalles_table.get_children():
                detalles_table.delete(detalle)

            try:
                cur.execute("""
                    SELECT v.idVenta, c.persona, CONCAT(u.nombre, ' ', u.apellido) AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.idUsuario = u.id_usuario
                    WHERE c.persona LIKE %s;
                """, ('%' + cliente + '%',))
                ventas = cur.fetchall()

                for venta in ventas:
                    table.insert("", "end", values=venta)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo buscar las ventas del cliente: {e}")

        def buscar_venta_por_trabajador():
            """Busca ventas por trabajador y muestra los resultados en la tabla."""
            global trabajador_entry, table, detalles_table

            trabajador = trabajador_entry.get().strip()
            if not trabajador:
                messagebox.showwarning("Advertencia", "Ingrese un nombre de trabajador válido.")
                return

            for item in table.get_children():
                table.delete(item)

            for detalle in detalles_table.get_children():
                detalles_table.delete(detalle)

            try:
                cur.execute("""
                    SELECT v.idVenta, c.persona, CONCAT(u.nombre, ' ', u.apellido) AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.idUsuario = u.id_usuario
                    WHERE CONCAT(u.nombre, ' ', u.apellido) LIKE %s;
                """, ('%' + trabajador + '%',))
                ventas = cur.fetchall()

                for venta in ventas:
                    table.insert("", "end", values=venta)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo buscar las ventas del trabajador: {e}")
                
        def mostrar_detalles(event):
            selected_item = table.selection()
            if not selected_item:
                return
            venta_id = table.item(selected_item, "values")[0]
            for item in detalles_table.get_children():
                detalles_table.delete(item)
            try:
                cur.execute("""
                    SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.cantidad * dv.precio_unitario AS subtotal
                    FROM detalle_venta AS dv
                    JOIN Producto AS p ON dv.Producto_idProducto = p.idProducto
                    WHERE dv.Venta_idVenta = %s
                """, (venta_id,))
                detalles = cur.fetchall()
                for detalle in detalles:
                    detalles_table.insert("", "end", values=detalle)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los detalles: {e}")

        # Función Eliminar
        def eliminar_venta_id():
            """Elimina una venta por ID."""
            global id_entry, table

            venta_id = id_entry.get().strip()
            if not venta_id or not venta_id.isdigit():
                messagebox.showwarning("Advertencia", "Ingrese un ID de venta válido.")
                return

            confirm = messagebox.askyesno("Confirmación", f"¿Está seguro de eliminar la venta con ID {venta_id}?")
            if not confirm:
                return

            try:
                cur.execute("SELECT idVenta FROM Venta WHERE idVenta = %s", (venta_id,))
                if not cur.fetchone():
                    messagebox.showwarning("Advertencia", "La venta no existe.")
                    return

                cur.execute("DELETE FROM detalle_venta WHERE Venta_idVenta = %s", (venta_id,))
                cur.execute("DELETE FROM Venta WHERE idVenta = %s", (venta_id,))
                cur.connection.commit()
                messagebox.showinfo("Éxito", "Venta eliminada exitosamente.")
                cargar_ventas()

            except Exception as e:
                cur.connection.rollback()
                messagebox.showerror("Error", f"Error al eliminar la venta: {e}")




        def agregar_venta():
            """Función que abre la ventana para ingresar la contraseña y acceder a la venta."""
            # Crear una ventana emergente para ingresar la contraseña
            password_window = ctk.CTkToplevel(base)
            password_window.title("Acceso a la Venta")
            password_window.geometry("400x200")
    
            # Centrar la ventana
            window_width = 400
            window_height = 200
            screen_width = password_window.winfo_screenwidth()
            screen_height = password_window.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_left = int(screen_width / 2 - window_width / 2)
            password_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
            # Poner la ventana al frente usando el atributo -topmost
            password_window.attributes("-topmost", True)  # Esta opción coloca la ventana al frente
            password_window.after(100, lambda: password_window.attributes("-topmost", False))  # Después de 100ms, quitar el atributo -topmost

    
            # Etiqueta y campo de entrada para la contraseña
            password_label = ctk.CTkLabel(password_window, text="Ingrese la Contraseña:", font=("Comic Sans MS", 14))
            password_label.pack(pady=10)

            password_entry = ctk.CTkEntry(password_window, show="*", width=250)
            password_entry.pack(pady=10)

            def mostrar_tabla_productos(user_id):
                """Función para mostrar la tabla de productos y gestionar la venta."""
                for widget in frame_light_gray.winfo_children():
                    widget.destroy()

                title_label = ctk.CTkLabel(frame_light_gray, text="Productos Disponibles", font=("Comic Sans MS", 30, "bold"))
                title_label.pack(pady=20)

                product_table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white")
                product_table_frame.pack(pady=20, fill="both", expand=True, padx=20)

                columns = ("idProducto", "Nombre", "Código", "Ubicación", "Precio", "Stock Actual", "Cantidad")
                product_table = ttk.Treeview(product_table_frame, columns=columns, show="headings", height=15)
                product_table.pack(fill="both", expand=True)

                style = ttk.Style()
                style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"), background="#D04A5D", foreground="black")
                style.configure("Treeview", rowheight=25, background="white", foreground="black", bordercolor="black", borderwidth=1)

                for col in columns:
                    product_table.heading(col, text=col)
                    product_table.column(col, anchor="center")
                
                product_table.column("idProducto", width=80, anchor="center")  # idProducto más estrecha
                product_table.column("Nombre", width=200, anchor="center")  # Nombre más ancha
                product_table.column("Código", width=100, anchor="center")  # Código
                product_table.column("Ubicación", width=150, anchor="center")  # Ubicación
                product_table.column("Precio", width=100, anchor="center")  # Precio alineado a la derecha
                product_table.column("Stock Actual", width=120, anchor="center")  # Stock
                product_table.column("Cantidad", width=80, anchor="center")

                try:
                    cur.execute("SELECT idProducto, nombre, codigo, Ubicacion_idUbicacion, valor_venta, stock_actual FROM Producto")
                    productos = cur.fetchall()
                    for producto in productos:
                        product_table.insert("", "end", values=(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5], 0))
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")

                def on_double_click(event):
                    """Permite editar la celda de la columna 'Cantidad'."""
                    item_id = product_table.identify_row(event.y)
                    column_id = product_table.identify_column(event.x)

                    if column_id == "#7":  # Columna 'Cantidad'
                        selected_item = product_table.item(item_id)
                        stock_actual = int(selected_item["values"][5])  # Stock Actual

                        col_bbox = product_table.bbox(item_id, column=column_id)  # Obtiene las coordenadas de la celda
                        if col_bbox:
                            x, y, _, _ = col_bbox  

                            x_offset = product_table.winfo_x()  # Ajuste horizontal relativo al contenedor del Treeview
                            y_offset = product_table.winfo_y() 

                            entry = ttk.Entry(product_table)
                            entry.place(x=x + x_offset, y=y + y_offset, width=100, height=25)  # Usa las coordenadas relativas

                            def save_edit(event):
                                """Guarda el valor ingresado y valida la cantidad."""
                                new_value = entry.get()
                                if not new_value.isdigit():
                                    messagebox.showerror("Error", "La cantidad debe ser un número entero.")
                                    new_value = 0
                                else:
                                    new_value = int(new_value)
                                    if new_value > stock_actual or new_value < 0:
                                        messagebox.showerror("Error", "La cantidad debe ser menor o igual al stock actual y mayor o igual a 0.")
                                        new_value = 0

                                product_table.set(item_id, column="Cantidad", value=new_value)
                                entry.destroy()

                            entry.bind("<Return>", save_edit)
                            entry.bind("<FocusOut>", save_edit)
                            entry.focus()

                product_table.bind("<Double-1>", on_double_click)


                def confirmar_venta():
                    """Confirma la venta, registra los datos en la base de datos y genera automáticamente una factura."""
                    total_importe = 0
                    productos_seleccionados = []

                    # Recolectar productos seleccionados con cantidades mayores a 0
                    for item in product_table.get_children():
                        values = product_table.item(item, "values")
                        cantidad = int(values[6])  # Columna Cantidad
                        precio = float(values[4])  # Columna Precio

                        if cantidad > 0:  # Solo procesar productos con cantidades válidas
                            productos_seleccionados.append((values[0], cantidad, precio))  # idProducto, cantidad, precio
                            total_importe += cantidad * precio

                    if not productos_seleccionados:
                        messagebox.showwarning("Advertencia", "Debe seleccionar al menos un producto con cantidad válida.")
                        return

                    # Crear una ventana emergente para seleccionar al cliente
                    select_client_window = ctk.CTkToplevel(base)
                    select_client_window.title("Seleccionar Cliente")
                    select_client_window.geometry("600x400")  # Tamaño de la ventana
                    select_client_window.resizable(False, False)

                    # Centrar la ventana
                    window_width = 600
                    window_height = 400
                    screen_width = select_client_window.winfo_screenwidth()
                    screen_height = select_client_window.winfo_screenheight()
                    position_top = int(screen_height / 2 - window_height / 2)
                    position_left = int(screen_width / 2 - window_width / 2)
                    select_client_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
                    select_client_window.lift()  # Poner la ventana al frente

                    # Crear el Treeview para mostrar los clientes
                    columns = ("idCliente", "Nombre")
                    client_table = ttk.Treeview(select_client_window, columns=columns, show="headings", height=15)
                    client_table.pack(fill="both", expand=True, padx=20, pady=20)

                    client_table.heading("idCliente", text="ID")
                    client_table.heading("Nombre", text="Nombre")
                    client_table.column("idCliente", width=50, anchor="center")
                    client_table.column("Nombre", width=250, anchor="center")

                    # Agregar barra de desplazamiento
                    scrollbar = ctk.CTkScrollbar(select_client_window, command=client_table.yview)
                    scrollbar.pack(side="right", fill="y")
                    client_table.configure(yscrollcommand=scrollbar.set)

                    try:
                        # Obtener los clientes de la base de datos
                        cur.execute("SELECT idCliente, persona FROM Cliente")
                        clientes = cur.fetchall()

                        for cliente in clientes:
                            client_table.insert("", "end", values=(cliente[0], cliente[1]))

                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudieron cargar los clientes: {e}")
                        select_client_window.destroy()
                        return

                    def seleccionar_cliente(event):
                        """Selecciona el cliente y cierra la ventana"""
                        selected_item = client_table.selection()
                        if not selected_item:
                            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente.")
                            return

                        cliente_id = client_table.item(selected_item)["values"][0]  # Obtener el idCliente
                        cliente_nombre = client_table.item(selected_item)["values"][1]  # Obtener el nombre del cliente

                        # Mostrar el nombre del cliente seleccionado (opcional)
                        messagebox.showinfo("Cliente Seleccionado", f"Cliente: {cliente_nombre} (ID: {cliente_id})")

                        # Cerrar la ventana de selección de cliente
                        select_client_window.destroy()

                        # Proceder con la venta
                        try:
                            # Obtener el próximo ID de venta
                            cur.execute("SELECT COALESCE(MAX(idVenta), 0) + 1 FROM Venta")
                            id_venta = cur.fetchone()[0]

                            # Calcular los totales
                            igv = 0.18
                            importe_total_igv = total_importe * (1 + igv)  # Precio con IGV
                            importe_total = total_importe  # Precio sin IGV

                            # Insertar la venta en la tabla Venta
                            cur.execute("""
                                INSERT INTO Venta (idVenta, fecha, Cliente_idCliente, descuento, importe_total, importe_total_igv, idUsuario)
                                VALUES (%s, NOW(), %s, %s, %s, %s, %s)
                            """, (id_venta, cliente_id, 0, importe_total, importe_total_igv, user_id))

                            # Insertar los productos en la tabla detalle_venta
                            cur.execute("SELECT COALESCE(MAX(iddetalle_venta), 0) + 1 FROM detalle_venta")
                            next_id_detalle = cur.fetchone()[0]

                            for prod_id, cantidad, precio in productos_seleccionados:
                                cur.execute("""
                                    INSERT INTO detalle_venta (iddetalle_venta, Venta_idVenta, Producto_idProducto, precio_unitario, cantidad)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (next_id_detalle, id_venta, prod_id, precio, cantidad))
                                next_id_detalle += 1

                                # Actualizar el stock y las salidas de los productos seleccionados
                                cur.execute("""
                                    UPDATE Producto 
                                    SET stock_actual = stock_actual - %s, salidas = salidas + %s
                                    WHERE idProducto = %s
                                """, (cantidad, cantidad, prod_id))

                            # Confirmar los cambios en la base de datos
                            cur.connection.commit()

                            # Generar automáticamente la factura
                            generar_factura_automatica(id_venta)

                            messagebox.showinfo("Éxito", "Venta confirmada y factura generada correctamente.")

                            # Reiniciar la tabla de productos (cantidades a 0)
                            mostrar_tabla_productos(user_id)

                        except Exception as e:
                            cur.connection.rollback()
                            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")

                    # Asociar la acción de selección de cliente al doble clic en una fila de la tabla
                    client_table.bind("<Double-1>", seleccionar_cliente)


                


                def cancelar_venta():
                    """Restablece todas las cantidades a 0."""
                    for item in product_table.get_children():
                        product_table.set(item, column="Cantidad", value=0)

                button_style = {
                    "width": 200,  # Tamaño del botón
                    "fg_color": "#D04A5D",  # Color de fondo del botón
                    "hover_color": "#B03B4A",  # Color de fondo al hacer hover
                    "font": ("Comic Sans MS", 14)  # Fuente
                }

                # Botón Confirmar Venta
                confirmar_button = ctk.CTkButton(
                    frame_light_gray,
                    text="Confirmar Venta",
                    command=confirmar_venta,
                    **button_style  # Aplicamos el estilo definido
                )
                confirmar_button.pack(side="left", padx=20, pady=20)

                # Botón Cancelar Venta
                cancelar_button = ctk.CTkButton(
                    frame_light_gray,
                    text="Cancelar Venta",
                    command=cancelar_venta,
                    **button_style  # Aplicamos el estilo definido
                )
                cancelar_button.pack(side="right", padx=20, pady=20)

            def verificar_contraseña():
                contraseña = password_entry.get().strip()
                if not contraseña:
                    messagebox.showwarning("Contraseña", "Por favor, ingrese una contraseña.")
                    return

                try:
                    cur.execute("SELECT id_usuario FROM usuarios WHERE contrasena = %s", (contraseña,))
                    user = cur.fetchone()
                    if user:
                        user_id = user[0]
                        password_window.destroy()
                        mostrar_tabla_productos(user_id)
                    else:
                        messagebox.showerror("Error", "Contraseña incorrecta.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo verificar la contraseña: {e}")

            verify_button = ctk.CTkButton(password_window, text="Verificar", command=verificar_contraseña, width=150)
            verify_button.pack(pady=10)

            close_button = ctk.CTkButton(password_window, text="Cancelar", command=password_window.destroy, width=150)
            close_button.pack(pady=10)
            
        def generar_factura_automatica(venta_id):
                    """Genera una factura automáticamente en una carpeta llamada Facturas."""
                    try:
                        # Crear carpeta Facturas si no existe
                        carpeta_facturas = "Facturas"
                        if not os.path.exists(carpeta_facturas):
                            os.makedirs(carpeta_facturas)

                        # Consultar la información de la venta
                        cur.execute("""
                            SELECT v.fecha, c.persona AS cliente, CONCAT(u.nombre, ' ', u.apellido) AS usuario, 
                                v.importe_total, v.importe_total_igv
                            FROM Venta AS v
                            JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                            JOIN usuarios AS u ON v.idUsuario = u.id_usuario
                            WHERE v.idVenta = %s;
                        """, (venta_id,))
                        venta = cur.fetchone()

                        # Consultar los detalles de la venta
                        cur.execute("""
                            SELECT p.nombre AS producto, dv.cantidad, dv.precio_unitario, 
                                (dv.cantidad * dv.precio_unitario) AS subtotal
                            FROM detalle_venta AS dv
                            JOIN Producto AS p ON dv.Producto_idProducto = p.idProducto
                            WHERE dv.Venta_idVenta = %s;
                        """, (venta_id,))
                        detalles = cur.fetchall()

                        # Ruta del archivo PDF
                        ruta_factura = os.path.join(carpeta_facturas, f"Factura_{venta_id}.pdf")

                        # Crear el archivo PDF
                        c = canvas.Canvas(ruta_factura, pagesize=letter)

                        # Insertar el logo
                        logo_path = "Imagenes/logo.png"
                        if os.path.exists(logo_path):
                            c.drawImage(logo_path, 50, 700, width=100, height=50, preserveAspectRatio=True, mask='auto')

                        # Encabezado
                        c.setFont("Helvetica-Bold", 20)
                        c.drawString(200, 750, "FACTURA")

                        c.setFont("Helvetica", 10)
                        c.drawString(50, 680, f"Fecha: {venta[0]}")  # Fecha
                        c.drawString(50, 660, f"Cliente: {venta[1]}")  # Cliente
                        c.drawString(50, 640, f"Atendido por: {venta[2]}")  # Usuario

                        # Tabla de detalles
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(50, 580, "DETALLES DE LA VENTA")
                        c.line(50, 570, 550, 570)

                        # Dibujar la tabla de productos
                        c.setFont("Helvetica-Bold", 10)
                        headers = ["Producto", "Cantidad", "Precio Unitario", "Subtotal"]
                        x_positions = [50, 250, 350, 450]  # Coordenadas X para las columnas
                        for i, header in enumerate(headers):
                            c.drawString(x_positions[i], 550, header)

                        c.line(50, 540, 550, 540)  # Línea horizontal debajo de los encabezados

                        # Añadir los productos a la tabla
                        y = 520
                        c.setFont("Helvetica", 8)
                        for detalle in detalles:
                            c.drawString(x_positions[0], y, detalle[0])  # Producto
                            c.drawString(x_positions[1], y, str(detalle[1]))  # Cantidad
                            c.drawString(x_positions[2], y, f"S/. {detalle[2]:.2f}")  # Precio Unitario
                            c.drawString(x_positions[3], y, f"S/. {detalle[3]:.2f}")  # Subtotal
                            y -= 20
                            if y < 50:  # Si no hay más espacio en la página, añadir una nueva página
                                c.showPage()
                                c.setFont("Helvetica", 8)
                                y = 750

                        # Totales
                        c.line(50, y - 10, 550, y - 10)  # Línea horizontal antes del total
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(350, y - 30, "TOTAL:")
                        c.drawString(450, y - 30, f"S/. {venta[3]:.2f}")  # Total sin IGV
                        c.drawString(350, y - 50, "TOTAL C/ IGV:")
                        c.drawString(450, y - 50, f"S/. {venta[4]:.2f}")  # Total con IGV

                        # Guardar el archivo PDF
                        c.save()

                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo generar la factura automáticamente: {e}")


        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        base = ctk.CTk()
        base.geometry("1200x600")
        base.title("Gestión de Ventas")

        screen_width = base.winfo_screenwidth()
        screen_height = base.winfo_screenheight()
        position_x = int((screen_width - 1200) / 2)
        position_y = int((screen_height - 600) / 2)
        base.geometry(f"1200x600+{position_x}+{position_y}")

        custom_color = "#D04A5D"

        frame_dark_gray = ctk.CTkFrame(base, width=300, height=600, fg_color='gray')
        frame_dark_gray.pack(side="left", fill="y")

        # Logo en la parte superior izquierda
        logo_image = Image.open("Imagenes/logo.png")  # Ruta de la imagen
        logo_image = logo_image.resize((250, 150), Image.LANCZOS)  # Redimensionar la imagen
        logo_image = ImageTk.PhotoImage(logo_image)
        logo_label = ctk.CTkLabel(frame_dark_gray, image=logo_image, text="")
        logo_label.image = logo_image  # Mantener referencia para evitar garbage collection
        logo_label.pack(pady=(20, 30))

        # Botones del menú izquierdo
        buttons = {
            "GESTIONAR VENTAS": mostrar_crud,  # Acción para mostrar la tabla de ventas
            "AGREGAR VENTA": agregar_venta,    # Acción para abrir ventana de verificación
            "REGRESAR": lambda: [base.destroy(), MainApp()]
        }

        for btn_text, btn_command in buttons.items():
            button = ctk.CTkButton(
                frame_dark_gray,
                text=btn_text,
                width=200,
                height=55,
                corner_radius=15,
                fg_color=custom_color,
                hover_color="#B03B4A",
                font=("Comic Sans MS", 14, "bold"),
                command=btn_command,
            )
            button.pack(pady=10, fill="x", padx=20)

        frame_light_gray = ctk.CTkFrame(base, width=900, height=600, fg_color='light gray')
        frame_light_gray.pack(side="right", fill="both", expand=True)

        title_label = ctk.CTkLabel(frame_light_gray, text="GESTIÓN DE VENTAS", font=("Comic Sans MS", 30, "bold"))
        title_label.pack(pady=20)

        search_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
        search_frame.pack(pady=10)

        id_label = ctk.CTkLabel(search_frame, text="ID Venta:", font=("Comic Sans MS", 14))
        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry = ctk.CTkEntry(search_frame, width=100)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar_venta, width=80, fg_color=custom_color, hover_color="#B03B4A")
        search_button.grid(row=0, column=2, padx=10, pady=5)

        delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_venta_id, width=80, fg_color=custom_color, hover_color="#B03B4A")
        delete_button.grid(row=0, column=3, padx=10, pady=5)

        table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white")
        table_frame.pack(pady=20, fill="x", padx=20)

        columns = ("ID Venta", "Cliente", "Usuario", "Fecha", "Total")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"), background=custom_color, foreground="black")
        style.configure("Treeview", rowheight=25, background="white", foreground="black", bordercolor="black", borderwidth=1)
        style.map("Treeview", background=[("selected", "#D04A5D")])

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center")

        detalles_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
        detalles_frame.pack(pady=10, fill="x", padx=20)

        detalles_text = ctk.CTkTextbox(detalles_frame, height=10, wrap="word")
        detalles_text.pack(fill="both", expand=True)

        mostrar_crud()
        base.mainloop()


if __name__ == "__main__":
    CRUDventas().crud()