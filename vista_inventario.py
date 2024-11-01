import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from gestionar_inventario import registrar_producto, actualizar_producto, consultar_producto, eliminar_producto
from conexion import miConexion, cur


class CRUDproductos:
    def crud():
        # Función para cargar todos los productos en la tabla
        def cargar_productos():
            for item in table.get_children():
                table.delete(item)
            try:
                # Actualiza la consulta SQL para incluir el nombre de la categoría
                cur.execute("""
                    SELECT p.idProducto, p.nombre, p.codigo, p.stock_actual, c.nombre 
                    FROM Producto AS p 
                    LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria 
                    LIMIT 0, 1000
                """)
                productos = cur.fetchall()
                for producto in productos:
                    table.insert("", "end", values=producto)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")

        # Función para buscar un producto por ID o nombre
        def buscar_producto():
            id_producto = id_entry.get().strip()
            nombre_producto = name_entry.get().strip()

            # Limpiar la tabla antes de mostrar los resultados de búsqueda
            for item in table.get_children():
                table.delete(item)

            try:
                if id_producto:
                    cur.execute("""
                        SELECT p.idProducto, p.nombre, p.codigo, p.stock_actual, c.nombre 
                        FROM Producto AS p 
                        LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria 
                        WHERE p.idProducto = %s
                    """, (id_producto,))
                elif nombre_producto:
                    cur.execute("""
                        SELECT p.idProducto, p.nombre, p.codigo, p.stock_actual, c.nombre 
                        FROM Producto AS p 
                        LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria 
                        WHERE p.nombre LIKE %s
                    """, (f"%{nombre_producto}%",))
                else:
                    cargar_productos()
                    return
                
                # Mostrar los resultados de búsqueda en la tabla
                productos = cur.fetchall()
                for producto in productos:
                    table.insert("", "end", values=producto)

                # Mostrar mensaje si no se encontró ningún producto
                if not productos:
                    messagebox.showinfo("Resultado", "No se encontraron productos con los criterios de búsqueda.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

        # Función para eliminar un producto por ID y recargar la tabla completa
        def eliminar_producto_id():
            id_producto = id_entry.get().strip()
            if not id_producto:
                messagebox.showinfo("Eliminar", "Ingrese un ID para eliminar.")
                return

            try:
                eliminar_producto(id_producto)  # Llamada a la función para eliminar el producto
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")

                # Eliminar el producto de la tabla visual sin recargar todos los datos
                for item in table.get_children():
                    producto = table.item(item, "values")
                    if producto[0] == id_producto:
                        table.delete(item)
                        break

                # Limpiar los campos de entrada y recargar la tabla completa
                id_entry.delete(0, ctk.END)
                name_entry.delete(0, ctk.END)
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

        # Función para manejar la selección de un producto en la tabla
        def seleccionar_producto(event):
            selected_item = table.focus()
            if selected_item:
                producto = table.item(selected_item, "values")
                id_entry.delete(0, ctk.END)
                id_entry.insert(0, producto[0])  # ID
                name_entry.delete(0, ctk.END)
                name_entry.insert(0, producto[1])  # Nombre

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        base = ctk.CTk()
        base.geometry("1100x600")
        base.title("CRUD Productos")

        screen_width = base.winfo_screenwidth()
        screen_height = base.winfo_screenheight()
        position_x = int((screen_width - 1100) / 2)
        position_y = int((screen_height - 600) / 2)
        base.geometry(f"1100x600+{position_x}+{position_y}")

        # Color personalizado para los botones y encabezados de la tabla
        custom_color = "#D04A5D"

        # Frame izquierdo plomo oscuro
        frame_dark_gray = ctk.CTkFrame(base, width=300, height=600, fg_color='gray')
        frame_dark_gray.pack(side="left", fill="y")
        logo = Image.open("Imagenes/logo.png")
        logo = logo.resize((250, 150), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = ctk.CTkLabel(frame_dark_gray, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=(20, 30))
        # Botones en el menú izquierdo
        buttons = ["VENTA", "REGISTRO VENTA", "CLIENTE", "PRODUCTO", "REGRESAR"]
        for btn_text in buttons:
            button = ctk.CTkButton(
                frame_dark_gray, 
                text=btn_text, 
                width=200, 
                height=50, 
                corner_radius=10, 
                fg_color=custom_color, 
                hover_color="#B03B4A", 
                font=("Comic Sans MS", 14, "bold")
            )
            button.pack(pady=10, fill="x", padx=20)

        # Frame derecho plomo claro
        frame_light_gray = ctk.CTkFrame(base, width=800, height=600, fg_color='light gray')
        frame_light_gray.pack(side="right", fill="both", expand=True)

        # Título en el frame derecho
        title_label = ctk.CTkLabel(frame_light_gray, text="INVENTARIO", font=("Comic Sans MS", 30, "bold"))
        title_label.pack(pady=20)

        # LabelFrame para búsqueda
        search_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
        search_frame.pack(pady=10)

        id_label = ctk.CTkLabel(search_frame, text="ID:", font=("Comic Sans MS", 14))
        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry = ctk.CTkEntry(search_frame, width=100)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        name_label = ctk.CTkLabel(search_frame, text="Nombre:", font=("Comic Sans MS", 14))
        name_label.grid(row=0, column=2, padx=5, pady=5)
        name_entry = ctk.CTkEntry(search_frame, width=275)
        name_entry.grid(row=0, column=3, padx=5, pady=5)

        search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar_producto, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
        search_button.grid(row=0, column=4, padx=10, pady=5)

        delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_producto_id, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
        delete_button.grid(row=0, column=5, padx=10, pady=5)

        # LabelFrame para la tabla de productos
        table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white", height=400)
        table_frame.pack(pady=20, fill="x", padx=20)

        # Actualiza las columnas para incluir el nombre de la categoría
        columns = ("ID", "Nombre", "Código", "Stock Actual", "Categoría")
        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        table.pack(fill="both", expand=True)

        # Estilos de la tabla para que los encabezados tengan fondo del color personalizado y el texto en blanco
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 10), background=custom_color, foreground="black")
        style.configure("Treeview", rowheight=25, background="white", foreground="black", bordercolor="black", borderwidth=1)
        style.map("Treeview", background=[("selected", "#D04A5D")])

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=150)

        # Evento para seleccionar un producto de la tabla
        table.bind("<ButtonRelease-1>", seleccionar_producto)

        cargar_productos()
        base.mainloop()

    crud()
