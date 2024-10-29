import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from gestionar_inventario import registrar_producto, actualizar_producto, consultar_producto, eliminar_producto
from conexion import miConexion, cur

def vista_producto():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    base = ctk.CTk()
    base.geometry("1300x700")
    base.title("Vista Producto")

    # Posicionar ventana al centro
    screen_width = base.winfo_screenwidth()
    screen_height = base.winfo_screenheight()
    position_x = int((screen_width - 1300) / 2)
    position_y = int((screen_height - 700) / 2)
    base.geometry(f"1300x700+{position_x}+{position_y}")

    # Color personalizado
    custom_color = "#D04A5D"

    # Frame izquierdo plomo oscuro
    frame_dark_gray = ctk.CTkFrame(base, width=300, height=700, fg_color='gray')
    frame_dark_gray.pack(side="left", fill="y")

    # Botones en el menú izquierdo
    buttons = ["NUEVA VENTA", "INVENTARIO", "VENTAS", "CLIENTES"]
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
    frame_light_gray = ctk.CTkFrame(base, width=1000, height=700, fg_color='light gray')
    frame_light_gray.pack(side="right", fill="both", expand=True)

    # Título en el frame derecho
    title_label = ctk.CTkLabel(frame_light_gray, text="INGRESAR PRODUCTO", font=("Comic Sans MS", 30, "bold"))
    title_label.pack(pady=20)

    # Sección para ingreso de producto nuevo
    producto_nuevo_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
    producto_nuevo_frame.pack(pady=10)

    # Función para cargar categorías al combobox
    def cargar_categorias():
        try:
            cur.execute("SELECT idCategoria, nombre FROM Categoria")
            return {categoria[1]: categoria[0] for categoria in cur.fetchall()}
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar las categorías: {e}")
            return {}

    categoria_dict = cargar_categorias()

    # Etiquetas y entradas para agregar producto
    ctk.CTkLabel(producto_nuevo_frame, text="Código:", font=("Comic Sans MS", 14)).grid(row=0, column=0, padx=5, pady=5)
    codigo_entry = ctk.CTkEntry(producto_nuevo_frame, width=150)
    codigo_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(producto_nuevo_frame, text="Artículo:", font=("Comic Sans MS", 14)).grid(row=0, column=2, padx=5, pady=5)
    nombre_entry = ctk.CTkEntry(producto_nuevo_frame, width=200)
    nombre_entry.grid(row=0, column=3, padx=5, pady=5)

    ctk.CTkLabel(producto_nuevo_frame, text="Valor Neto:", font=("Comic Sans MS", 14)).grid(row=1, column=0, padx=5, pady=5)
    valor_neto_entry = ctk.CTkEntry(producto_nuevo_frame, width=150)
    valor_neto_entry.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(producto_nuevo_frame, text="Valor de venta:", font=("Comic Sans MS", 14)).grid(row=1, column=2, padx=5, pady=5)
    valor_venta_entry = ctk.CTkEntry(producto_nuevo_frame, width=150)
    valor_venta_entry.grid(row=1, column=3, padx=5, pady=5)

    ctk.CTkLabel(producto_nuevo_frame, text="Categoría:", font=("Comic Sans MS", 14)).grid(row=1, column=4, padx=5, pady=5)
    categoria_combo = ttk.Combobox(producto_nuevo_frame, values=list(categoria_dict.keys()), state="readonly", width=15)
    categoria_combo.grid(row=1, column=5, padx=5, pady=5)

    ctk.CTkLabel(producto_nuevo_frame, text="Stock Actual:", font=("Comic Sans MS", 14)).grid(row=1, column=6, padx=5, pady=5)
    stock_entry = ctk.CTkEntry(producto_nuevo_frame, width=100)
    stock_entry.grid(row=1, column=7, padx=5, pady=5)

    # Botón para registrar el producto
    def registrar_producto_callback():
        codigo = codigo_entry.get()
        nombre = nombre_entry.get()
        valor_neto = valor_neto_entry.get()
        valor_venta = valor_venta_entry.get()
        categoria_nombre = categoria_combo.get()
        stock_actual = stock_entry.get()
        ubicacion = "Ubicación específica"  # puedes cambiar esto por el valor de otra entrada si deseas

        categoria_id = categoria_dict.get(categoria_nombre)

        try:
            registrar_producto(nombre, codigo, valor_neto, valor_venta, stock_actual, categoria_id, ubicacion)
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            cargar_productos()  # Actualizar la tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    agregar_producto_btn = ctk.CTkButton(producto_nuevo_frame, text="Registrar Producto", width=150, fg_color=custom_color, command=registrar_producto_callback)
    agregar_producto_btn.grid(row=2, columnspan=8, pady=20)

    # Tabla de productos
    table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white", height=300)
    table_frame.pack(pady=20, fill="x", padx=20)

    columns = ("CODIGO", "ARTICULO", "VALOR NETO", "VALOR DE VENTA", "CATEGORIA", "STOCK")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    table.pack(fill="both", expand=True)

    column_widths = [70, 150, 100, 100, 120, 80]
    for col, width in zip(columns, column_widths):
        table.heading(col, text=col)
        table.column(col, anchor="center", width=width)

    # Función para cargar los productos en la tabla
    def cargar_productos():
        for item in table.get_children():
            table.delete(item)
        try:
            cur.execute("""SELECT p.codigo, p.nombre, p.valor_neto, p.valor_venta, c.nombre, p.stock_actual
                           FROM Producto AS p 
                           LEFT JOIN Categoria AS c ON c.idCategoria = p.idCategoria""")
            productos = cur.fetchall()
            for producto in productos:
                table.insert("", "end", values=producto)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")

    # Sección para agregar stock adicional
    stock_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
    stock_frame.pack(pady=10)

    # Etiqueta y entrada para el código del producto
    ctk.CTkLabel(stock_frame, text="Código:", font=("Comic Sans MS", 14)).grid(row=0, column=0, padx=5, pady=5)
    codigo_stock_entry = ctk.CTkEntry(stock_frame, width=100)
    codigo_stock_entry.grid(row=0, column=1, padx=5, pady=5)

    # Etiqueta y entrada para la cantidad de stock a agregar
    ctk.CTkLabel(stock_frame, text="Stock a agregar:", font=("Comic Sans MS", 14)).grid(row=0, column=2, padx=5, pady=5)
    stock_add_entry = ctk.CTkEntry(stock_frame, width=100)
    stock_add_entry.grid(row=0, column=3, padx=5, pady=5)

    # Botón para agregar stock
    def agregar_stock():
        codigo = codigo_stock_entry.get().strip()  
        cantidad_a_agregar = stock_add_entry.get()
        if codigo and cantidad_a_agregar.isdigit():
            cantidad_a_agregar = int(cantidad_a_agregar)
            if cantidad_a_agregar > 0:
                try:
                    cur.execute("UPDATE Producto SET stock_actual = stock_actual + %s WHERE codigo = %s", (cantidad_a_agregar, codigo))
                    miConexion.commit()
                    cargar_productos()
                    messagebox.showinfo("Éxito", "Stock actualizado.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el stock: {e}")
            else:
                messagebox.showerror("Error", "Cantidad debe ser mayor a cero.")
        else:
            messagebox.showerror("Error", "Por favor, ingresa un código y cantidad válidos.")
            
    agregar_stock_btn = ctk.CTkButton(stock_frame, text="Agregar Stock", width=150, fg_color=custom_color, command=agregar_stock)
    agregar_stock_btn.grid(row=1, columnspan=4, pady=20)

    cargar_productos()

    base.mainloop()
