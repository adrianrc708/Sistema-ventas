import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from gestionar_clientes import consultar_cliente, eliminar_cliente,registrar_cliente
from conexion import miConexion, cur

class CRUDclientes:
    def crud():
        def cargar_clientes():
            for item in table.get_children():
                table.delete(item)
            try:
                cur.execute("SELECT idCliente, persona, direccion, telefono, DNI_RUC FROM Cliente")
                clientes = cur.fetchall()
                for cliente in clientes:
                    table.insert("", "end", values=cliente)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar los clientes: {e}")

        def buscar_cliente():
            id_cliente = id_entry.get().strip()
            nombre_cliente = name_entry.get().strip()
            dni_ruc = dni_entry.get().strip()

            for item in table.get_children():
                table.delete(item)
            
            try:
                if id_cliente:
                    cur.execute("SELECT idCliente, persona, direccion, telefono, DNI_RUC FROM Cliente WHERE idCliente = %s", (id_cliente,))
                elif nombre_cliente:
                    cur.execute("SELECT idCliente, persona, direccion, telefono, DNI_RUC FROM Cliente WHERE persona LIKE %s", (f"%{nombre_cliente}%",))
                elif dni_ruc:
                    cur.execute("SELECT idCliente, persona, direccion, telefono, DNI_RUC FROM Cliente WHERE DNI_RUC = %s", (dni_ruc,))
                else:
                    cargar_clientes()
                    return
                
                clientes = cur.fetchall()
                for cliente in clientes:
                    table.insert("", "end", values=cliente)
                
                if not clientes:
                    messagebox.showinfo("Resultado", "No se encontraron clientes con los criterios de búsqueda.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

        def eliminar_cliente_id():
            id_cliente = id_entry.get().strip()
            if not id_cliente:
                messagebox.showinfo("Eliminar", "Ingrese un ID para eliminar.")
                return

            try:
                eliminar_cliente(id_cliente)
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")

                for item in table.get_children():
                    cliente = table.item(item, "values")
                    if cliente[0] == id_cliente:
                        table.delete(item)
                        break

                id_entry.delete(0, ctk.END)
                name_entry.delete(0, ctk.END)
                dni_entry.delete(0, ctk.END)
                cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

        def seleccionar_cliente(event):
            selected_item = table.focus()
            if selected_item:
                cliente = table.item(selected_item, "values")
                id_entry.delete(0, ctk.END)
                id_entry.insert(0, cliente[0])
                name_entry.delete(0, ctk.END)
                name_entry.insert(0, cliente[1])
                dni_entry.delete(0, ctk.END)
                dni_entry.insert(0, cliente[4])

        def mostrar_interfaz_clientes():
            for widget in frame_light_gray.winfo_children():
                widget.destroy()

            title_label = ctk.CTkLabel(frame_light_gray, text="CLIENTES", font=("Comic Sans MS", 30, "bold"))
            title_label.pack(pady=20)

            search_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
            search_frame.pack(pady=10)

            global id_entry, name_entry, dni_entry, table

            id_label = ctk.CTkLabel(search_frame, text="ID:", font=("Comic Sans MS", 14))
            id_label.grid(row=0, column=0, padx=5, pady=5)
            id_entry = ctk.CTkEntry(search_frame, width=100)
            id_entry.grid(row=0, column=1, padx=5, pady=5)

            name_label = ctk.CTkLabel(search_frame, text="Nombre:", font=("Comic Sans MS", 14))
            name_label.grid(row=0, column=2, padx=5, pady=5)
            name_entry = ctk.CTkEntry(search_frame, width=150)
            name_entry.grid(row=0, column=3, padx=5, pady=5)

            dni_label = ctk.CTkLabel(search_frame, text="DNI/RUC:", font=("Comic Sans MS", 14))
            dni_label.grid(row=0, column=4, padx=5, pady=5)
            dni_entry = ctk.CTkEntry(search_frame, width=150)
            dni_entry.grid(row=0, column=5, padx=5, pady=5)

            search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar_cliente, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
            search_button.grid(row=0, column=6, padx=10, pady=5)

            delete_button = ctk.CTkButton(search_frame, text="Eliminar", command=eliminar_cliente_id, width=80, fg_color=custom_color, hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
            delete_button.grid(row=0, column=7, padx=10, pady=5)

            table_frame = ctk.CTkFrame(frame_light_gray, fg_color="white", height=400)
            table_frame.pack(pady=20, fill="x", padx=20)

            columns = ("ID", "Nombre", "Dirección", "Teléfono", "DNI/RUC")
            table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
            table.pack(fill="both", expand=True)

            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Comic Sans MS", 10,"bold"), background=custom_color, foreground="black")
            style.configure("Treeview", rowheight=25, background="white", foreground="black", bordercolor="black", borderwidth=1)
            style.map("Treeview", background=[("selected", "#D04A5D")])

            for col in columns:
                table.heading(col, text=col)
                table.column(col, anchor="center", width=150)

            table.bind("<ButtonRelease-1>", seleccionar_cliente)
            cargar_clientes()


        def registro():
            for widget in frame_light_gray.winfo_children():
                widget.destroy()

            title_label = ctk.CTkLabel(frame_light_gray, text="REGISTRAR CLIENTE", font=("Comic Sans MS", 30, "bold"))
            title_label.pack(pady=20)

            form_frame = ctk.CTkFrame(frame_light_gray, fg_color="light gray")
            form_frame.pack(pady=10, padx=20)

            # Campo para el nombre
            name_label = ctk.CTkLabel(form_frame, text="Nombre:", font=("Comic Sans MS", 14))
            name_label.grid(row=0, column=0, padx=10, pady=10)
            name_entry = ctk.CTkEntry(form_frame, width=200)
            name_entry.grid(row=0, column=1, padx=10, pady=10)

            # Campo para la dirección
            address_label = ctk.CTkLabel(form_frame, text="Dirección:", font=("Comic Sans MS", 14))
            address_label.grid(row=1, column=0, padx=10, pady=10)
            address_entry = ctk.CTkEntry(form_frame, width=200)
            address_entry.grid(row=1, column=1, padx=10, pady=10)

            # Campo para el teléfono
            phone_label = ctk.CTkLabel(form_frame, text="Teléfono:", font=("Comic Sans MS", 14))
            phone_label.grid(row=2, column=0, padx=10, pady=10)
            phone_entry = ctk.CTkEntry(form_frame, width=200)
            phone_entry.grid(row=2, column=1, padx=10, pady=10)

            # Campo para el DNI/RUC
            dni_label = ctk.CTkLabel(form_frame, text="DNI/RUC:", font=("Comic Sans MS", 14))
            dni_label.grid(row=3, column=0, padx=10, pady=10)
            dni_entry = ctk.CTkEntry(form_frame, width=200)
            dni_entry.grid(row=3, column=1, padx=10, pady=10)

            # Función para guardar el cliente en la base de datos
            def guardar_cliente():
                nombre = name_entry.get().strip()
                direccion = address_entry.get().strip()
                telefono = phone_entry.get().strip()
                dni_ruc = dni_entry.get().strip()

                if not nombre or not direccion or not telefono or not dni_ruc:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                try:
                    registrar_cliente(nombre, direccion, telefono, dni_ruc)
                    messagebox.showinfo("Éxito", "Cliente registrado exitosamente.")
                    name_entry.delete(0, ctk.END)
                    address_entry.delete(0, ctk.END)
                    phone_entry.delete(0, ctk.END)
                    dni_entry.delete(0, ctk.END)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

            # Botón para guardar el cliente
            save_button = ctk.CTkButton(form_frame, text="Guardar", command=guardar_cliente, width=150, fg_color="#D04A5D", hover_color="#B03B4A", font=("Comic Sans MS", 14, "bold"))
            save_button.grid(row=4, column=0, columnspan=2, pady=20)





        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        base = ctk.CTk()
        base.geometry("1100x600")
        base.title("CRUD Clientes")

        screen_width = base.winfo_screenwidth()
        screen_height = base.winfo_screenheight()
        position_x = int((screen_width - 1100) / 2)
        position_y = int((screen_height - 600) / 2)
        base.geometry(f"1100x600+{position_x}+{position_y}")

        custom_color = "#D04A5D"

        frame_dark_gray = ctk.CTkFrame(base, width=300, height=600, fg_color='gray')
        frame_dark_gray.pack(side="left", fill="y")

        logo = Image.open("Imagenes/logo.png")
        logo = logo.resize((250, 150), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = ctk.CTkLabel(frame_dark_gray, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=(20, 30))

        buttons = {"REGISTRAR CLIENTE": registro, "CLIENTES": mostrar_interfaz_clientes, "REGRESAR": base.quit}
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
                command=btn_command
            )
            button.pack(pady=10, fill="x", padx=20)

        frame_light_gray = ctk.CTkFrame(base, width=800, height=600, fg_color='light gray')
        frame_light_gray.pack(side="right", fill="both", expand=True)

        mostrar_interfaz_clientes()
        base.mainloop()

    crud()
