import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from gestionar_ventas import registrar_venta, consultar_venta, eliminar_venta
from conexion import cur


class CRUDventas:
    def crud(self):
        def cargar_ventas():
            for item in table.get_children():
                table.delete(item)
            try:
                cur.execute("""
                    SELECT v.idVenta, c.persona, CONCAT(u.nombre, ' ', u.apellido) AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.idUsuario = u.id_usuario;
                """)
                ventas = cur.fetchall()
                for venta in ventas:
                    table.insert("", "end", values=venta)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar las ventas: {e}")

        def buscar_venta():
            venta_id = id_entry.get().strip()
            for item in table.get_children():
                table.delete(item)
            try:
                if venta_id:
                    venta, detalles = consultar_venta(venta_id)

                    if venta:
                        # Limpia el campo de texto antes de agregar detalles
                        detalles_text.delete(1.0, ctk.END)

                        # Inserta los datos de la venta en la tabla
                        table.insert("", "end", values=(venta[0], venta[1], f"{venta[2]} {venta[3]}", venta[4], venta[6]))

                        # Inserta los detalles en el campo de texto
                        detalles_text.insert(ctk.END, "Detalles de la Venta:\n")
                        for detalle in detalles:
                            detalles_text.insert(
                                ctk.END,
                                f"- Producto: {detalle[0]}, Cantidad: {detalle[1]}, Precio Unitario: {detalle[2]}, Subtotal: {detalle[3]:.2f}\n"
                            )
                    else:
                        detalles_text.delete(1.0, ctk.END)
                        detalles_text.insert(ctk.END, "No se encontró la venta.\n")
                        messagebox.showinfo("Resultado", "No se encontró la venta.")
                else:
                    cargar_ventas()
            except Exception as e:
                detalles_text.delete(1.0, ctk.END)
                detalles_text.insert(ctk.END, "Ocurrió un error al buscar la venta.\n")
                messagebox.showerror("Error", f"No se pudo buscar la venta: {e}")



        def eliminar_venta_id():
            venta_id = id_entry.get().strip()
            if not venta_id:
                messagebox.showinfo("Eliminar", "Ingrese un ID para eliminar.")
                return
            try:
                eliminar_venta(venta_id)
                messagebox.showinfo("Éxito", "Venta eliminada exitosamente.")
                cargar_ventas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la venta: {e}")

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
            "AGREGAR VENTA": lambda: messagebox.showinfo("Acción", "Agregar Venta"),
            "FACTURACIÓN": lambda: messagebox.showinfo("Acción", "Facturación"),
            "REGRESAR": base.destroy,
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

        cargar_ventas()
        base.mainloop()


if __name__ == "__main__":
    CRUDventas().crud()
