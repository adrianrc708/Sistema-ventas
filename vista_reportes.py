from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

from conexion import miConexion, cur
from generar_reportes import reporte_ventas, reporte_inventario, ventas_por_cliente

class CRUDReportes:
    def __init__(self):
        self.crud()

    def crud(self):
        from main import MainApp
        # Configuración y creación de la interfaz gráfica
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        base = ctk.CTk()
        base.geometry("1300x700")
        base.title("CRUD Productos")

        # Centrar ventana
        screen_width = base.winfo_screenwidth()
        screen_height = base.winfo_screenheight()
        position_x = int((screen_width - 1300) / 2)
        position_y = int((screen_height - 700) / 2)
        base.geometry(f"1300x700+{position_x}+{position_y}")

        custom_color = "#D04A5D"

        # Frame izquierdo
        frame_dark_gray = ctk.CTkFrame(base, width=300, height=700, fg_color='gray')
        frame_dark_gray.pack(side="left", fill="y")
        logo = Image.open("Imagenes/logo.png")
        logo = logo.resize((250, 150), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = ctk.CTkLabel(frame_dark_gray, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=(20, 30))

        #Frame derecho para tabla de productos
        frame_light_gray = ctk.CTkFrame(base, width=1000, height=700, fg_color='light gray')
        frame_light_gray.pack(side="right", fill="both", expand=True)
        

        # Funciones para manejar productos
        def mostrar_datos_en_tabla(datos, columnas):
            table.delete(*table.get_children())
            table["columns"] = columnas
            for col in columnas:
                table.heading(col, text=col)
                table.column(col, anchor="center", stretch=True, width=int(table_frame.winfo_width() / len(columnas)))
            for fila in datos:
                table.insert("", "end", values=fila)

        # Función para mostrar reporte de ventas
        def mostrar_reporte_ventas():
            try:
                datos = reporte_ventas()
                columnas = ["Cliente", "Número de Compras"]
                if not datos:
                    table.delete(*table.get_children())
                    texto_label.configure(text="NO HAY CLIENTES RECURRENTES", font=("Comic Sans MS", 20, "bold"))
                    button_mostrar_ventas.pack_forget()
                else:
                    mostrar_datos_en_tabla(datos, columnas)
                    texto_label.configure(text="CLIENTES RECURRENTES", font=("Comic Sans MS", 20, "bold"))
                    button_mostrar_ventas.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el reporte de ventas: {e}")

        # Función para mostrar reporte de inventario
        def mostrar_reporte_inventario():
            try:
                datos = reporte_inventario()  # Llamamos a la función de generar_reportes
                columnas = ["Producto","Stock"]
                if not datos:
                    table.delete(*table.get_children())
                    texto_label.configure(text="NO HAY PRODUCTOS CON STOCK LIMITADO", font=("Comic Sans MS", 20, "bold"))
                    button_mostrar_ventas.pack_forget()
                else:
                    mostrar_datos_en_tabla(datos, columnas)
                    texto_label.configure(text="PRODUCTOS CON STOCK LIMITADO", font=("Comic Sans MS", 20, "bold"))
                    button_mostrar_ventas.pack_forget()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el reporte de inventario: {e}")

        def mostrar_ventas_cliente():
            # Obtener el cliente seleccionado en la tabla
            seleccion = table.selection()
            if seleccion:
                cliente_seleccionado = table.item(seleccion[0])['values'][0]
                ventas = ventas_por_cliente(cliente_seleccionado)
                columnas_ventas = ["ID","Fecha", "Producto", "Cantidad"]
                mostrar_datos_en_tabla(ventas, columnas_ventas)
                texto_label.configure(text=f"Ventas de {cliente_seleccionado}", font=("Comic Sans MS", 20, "bold"))
                button_mostrar_ventas.pack_forget()
            else:
                messagebox.showwarning("Selección inválida", "Por favor, seleccione un cliente.")
        # Botones de funcionalidades
        buttons = [
            ("REPORTE VENTAS", mostrar_reporte_ventas),
            ("REPORTE INVENTARIO", mostrar_reporte_inventario),
            ("REGRESAR", lambda: [base.destroy(), MainApp()]),
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

        # Frame derecho para la tabla de productos

        title_label = ctk.CTkLabel(frame_light_gray, text="REPORTES", font=("Comic Sans MS", 30, "bold"))
        title_label.pack(pady=20)

        # texto del subtítulo 
        texto_label = ctk.CTkLabel(frame_light_gray, text="", font=("Consola", 14))
        texto_label.pack(pady=10)

        table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white", height=500)
        table_frame.pack(pady=20, fill="x", padx=20)


        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 12, "bold"))
        style.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25)
        
        table = ttk.Treeview(table_frame, show="headings", height=20)
        table.pack(fill="both", expand=True)

        button_mostrar_ventas = ctk.CTkButton(
            frame_light_gray, 
            text="Mostrar Ventas del Cliente", 
            width=200, 
            height=50, 
            corner_radius=10, 
            fg_color=custom_color, 
            hover_color="#B03B4A", 
            font=("Comic Sans MS", 14, "bold"),
            command=mostrar_ventas_cliente
        )
        button_mostrar_ventas.pack_forget()
        base.mainloop()


if __name__ == "__main__":
   CRUDReportes()