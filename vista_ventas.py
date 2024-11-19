import customtkinter as ctk
from tkinter import ttk, messagebox
from gestionar_ventas import registrar_venta, consultar_venta, eliminar_venta
from conexion import cur

class CRUDventas:
    def crud(self):
        def cargar_ventas():
            for item in table.get_children():
                table.delete(item)
            try:
                cur.execute("""
                    SELECT v.idVenta, c.persona, u.nombre || ' ' || u.apellido AS usuario, v.fecha, v.importe_total
                    FROM Venta AS v
                    JOIN Cliente AS c ON v.Cliente_idCliente = c.idCliente
                    JOIN usuarios AS u ON v.Usuario_idUsuario = u.id_usuario
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
                        detalles_text.delete(1.0, ctk.END)
                        table.insert("", "end", values=(venta[0], venta[1], f"{venta[2]} {venta[3]}", venta[4], venta[6]))
                        detalles_text.insert(ctk.END, "Detalles de la Venta:\n")
                        for detalle in detalles:
                            detalles_text.insert(ctk.END, f"{detalle[0]}: {detalle[1]} x {detalle[2]} = {detalle[3]:.2f}\n")
                    else:
                        messagebox.showinfo("Resultado", "No se encontró la venta.")
                else:
                    cargar_ventas()
            except Exception as e:
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

        frame_left = ctk.CTkFrame(base, width=300, height=600, fg_color='gray')
        frame_left.pack(side="left", fill="y")

        frame_right = ctk.CTkFrame(base, width=900, height=600, fg_color='light gray')
        frame_right.pack(side="right", fill="both", expand=True)

        title_label = ctk.CTkLabel(frame_right, text="Gestión de Ventas", font=("Comic Sans MS", 30, "bold"))
        title_label.pack(pady=20)

        search_frame = ctk.CTkFrame(frame_right, fg_color="light gray")
        search_frame.pack(pady=10)

        id_label = ctk.CTkLabel(search_frame, text="ID Venta:", font=("Comic Sans MS", 14))
        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry = ctk.CTkEntry(search_frame, width=100)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar_venta, width=80, fg_color="#D04A5D")
        search_button.grid(row=0, column=2, padx=10, pady=5)

        delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_venta_id, width=80, fg_color="#D04A5D")
        delete_button.grid(row=0, column=3, padx=10, pady=5)

        table_frame = ctk.CTkFrame(frame_right, fg_color="white")
        table_frame.pack(pady=20, fill="x", padx=20)

        columns = ("ID Venta", "Cliente", "Usuario", "Fecha", "Total")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center")

        detalles_frame = ctk.CTkFrame(frame_right, fg_color="light gray")
        detalles_frame.pack(pady=10, fill="x", padx=20)

        detalles_text = ctk.CTkTextbox(detalles_frame, height=10, wrap="word")
        detalles_text.pack(fill="both", expand=True)

        cargar_ventas()
        base.mainloop()
        
if __name__ == "__main__":
    CRUDventas().crud()
