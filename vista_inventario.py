from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from gestionar_inventario import eliminar_producto
from vista_producto import vista_producto
from conexion import miConexion, cur


class CRUDproductos:
    def _init_(self):
        self.crud()

    def crud(self):
        from main import MainApp
        def cargar_productos():
            for item in table.get_children():
                table.delete(item)
            try:
                cur.execute("""
                    SELECT p.codigo, p.nombre,p.valor_neto, p.valor_venta, c.nombre , u.ubicacion, p.entradas, p.salidas, stock_actual
                    FROM Producto AS p 
                    LEFT JOIN Categoria AS c ON c.idCategoria = p.idCategoria
                    LEFT JOIN UbicacionProducto AS u ON u.idUbicacion = p.Ubicacion_idUbicacion
                    LIMIT 0, 1000;
                """)
                productos = cur.fetchall()
                for producto in productos:
                    table.insert("", "end", values=producto)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")

        def buscar_producto():
            id_producto = id_entry.get().strip()
            nombre_producto = name_entry.get().strip()
            for item in table.get_children():
                table.delete(item)
            try:
                if id_producto:
                    cur.execute("""
                        SELECT p.codigo, p.nombre, p.valor_neto, p.valor_venta, c.nombre, u.ubicacion, p.entradas, p.salidas, p.stock_actual 
                        FROM Producto AS p 
                        LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria 
                        LEFT JOIN UbicacionProducto AS u ON p.Ubicacion_idUbicacion = u.idUbicacion 
                        WHERE p.codigo = %s
                    """, (id_producto,))
                elif nombre_producto:
                    cur.execute("""
                        SELECT p.codigo, p.nombre, p.valor_neto, p.valor_venta, c.nombre, u.ubicacion, p.entradas, p.salidas, p.stock_actual 
                        FROM Producto AS p 
                        LEFT JOIN Categoria AS c ON p.idCategoria = c.idCategoria 
                        LEFT JOIN UbicacionProducto AS u ON p.Ubicacion_idUbicacion = u.idUbicacion 
                        WHERE p.nombre LIKE %s
                    """, (f"%{nombre_producto}%",))
                else:
                    cargar_productos()
                    return
                productos = cur.fetchall()
                if productos:
                    for producto in productos:
                        table.insert("", "end", values=producto)
                else:
                    messagebox.showinfo("Resultado", "No se encontraron productos con los criterios de búsqueda.")
                    cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

        def eliminar_producto_codigo():
            codigo = id_entry.get().strip()
            if not codigo:
                messagebox.showinfo("Eliminar", "Ingrese un código para eliminar.")
                return

            try:
                eliminar_producto(codigo)
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")

                for item in table.get_children():
                    producto = table.item(item, "values")
                    if producto[0] == codigo:
                        table.delete(item)
                        break

                id_entry.delete(0, ctk.END)
                name_entry.delete(0, ctk.END)
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

        def seleccionar_producto(event):
            selected_item = table.focus()
            if selected_item:
                producto = table.item(selected_item, "values")
                id_entry.delete(0, ctk.END)
                id_entry.insert(0, producto[0])
                name_entry.delete(0, ctk.END)
                name_entry.insert(0, producto[1])

        def regresar_main():
            base.destroy()  # Cierra la ventana actual
            MainApp()  # Inicia una nueva instancia de MainApp

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        base = ctk.CTk()
        base.geometry("1300x600")
        base.title("CRUD Productos")

        screen_width = base.winfo_screenwidth()
        screen_height = base.winfo_screenheight()
        position_x = int((screen_width - 1300) / 2)
        position_y = int((screen_height - 600) / 2)
        base.geometry(f"1300x600+{position_x}+{position_y}")

        custom_color = "#D04A5D"

        frame_dark_gray = ctk.CTkFrame(base, width=300, height=600, fg_color='gray')
        frame_dark_gray.pack(side="left", fill="y")
        logo = Image.open("Imagenes/logo.png")
        logo = logo.resize((250, 150), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = ctk.CTkLabel(frame_dark_gray, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=(20, 30))

        # Reemplazar botones sin función por AGREGAR PRODUCTO y REGRESAR
        buttons = [
            ("AGREGAR PRODUCTO", lambda: [base.destroy(), vista_producto()]),
            ("REGRESAR", regresar_main)
        ]
        for btn_text, btn_command in buttons:
            button = ctk.CTkButton(
                frame_dark_gray,
                text=btn_text,
                width=200,
                height=50,
                corner_radius=10,
                fg_color=custom_color,
                hover_color="#B03B4A",
                font=("Comic Sans MS", 14, "bold"),
                command=btn_command
            )
            button.pack(pady=10, fill="x", padx=20)

        frame_light_gray = ctk.CTkFrame(base, width=1000, height=700, fg_color='light gray')
        frame_light_gray.pack(side="right", fill="both", expand=True)

        title_label = ctk.CTkLabel(frame_light_gray, text="INVENTARIO", font=("Comic Sans MS", 40, "bold"))
        title_label.pack(pady=20)

        search_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
        search_frame.pack(pady=10)

        id_label = ctk.CTkLabel(search_frame, text="Codigo:", font=("Comic Sans MS", 14))
        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry = ctk.CTkEntry(search_frame, width=100)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        name_label = ctk.CTkLabel(search_frame, text="Nombre:", font=("Comic Sans MS", 14))
        name_label.grid(row=0, column=2, padx=5, pady=5)
        name_entry = ctk.CTkEntry(search_frame, width=275)
        name_entry.grid(row=0, column=3, padx=5, pady=5)

        search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar_producto, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
        search_button.grid(row=0, column=4, padx=10, pady=5)

        delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_producto_codigo, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
        delete_button.grid(row=0, column=5, padx=10, pady=5)

        table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white", height=500)
        table_frame.pack(pady=20, fill="x", padx=20)

        columns = ("CODIGO", "ARTICULO", "VALOR NETO", "VALOR DE VENTA", "CATEGORIA", "UBICACION", "ENTRADAS", "SALIDAS", "STOCK")
        column_widths = {
            "CODIGO": 70,
            "ARTICULO": 240,
            "VALOR NETO": 100,
            "VALOR DE VENTA": 100,
            "CATEGORIA": 120,
            "UBICACION": 70,
            "ENTRADAS": 100,
            "SALIDAS": 100,
            "STOCK": 50,
        }

        table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 11, "bold"), background=custom_color, foreground="black")
        style.configure("Treeview", font=("Comic Sans MS", 11), rowheight=25, background="white", foreground="black", bordercolor="black", borderwidth=3)
        style.map("Treeview", background=[("selected", "#D04A5D")])

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=column_widths[col])

        table.bind("<ButtonRelease-1>", seleccionar_producto)

        cargar_productos()
        base.mainloop()

if __name__ == "__main__":
    CRUDproductos().crud()