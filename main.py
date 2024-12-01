import customtkinter as ctk
from PIL import Image, ImageTk
from controlador import Controlador  # Asegúrate de importar el Controlador correctamente

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.geometry("400x500")
        self.root.title("Sistema de Gestión")

        # Centrar la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = int((screen_width - 400) / 2)
        position_y = int((screen_height - 500) / 2)
        self.root.geometry(f"400x500+{position_x}+{position_y}")

        # Fondo plomo
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#D3D3D3", width=400, height=500)  # Color plomo
        self.main_frame.pack(fill="both", expand=True)

        self.add_logo()
        self.create_main_buttons()
        self.root.mainloop()

    def add_logo(self):
        try:
            logo = Image.open("Imagenes/logo.png")
            logo = logo.resize((200, 100), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo)
            logo_label = ctk.CTkLabel(self.main_frame, image=self.logo_image, text="", fg_color="#D3D3D3")
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            logo_label = ctk.CTkLabel(self.main_frame, text="Logo Aquí", font=("Comic Sans MS", 14, "bold"))
            logo_label.pack(pady=20)

    def create_main_buttons(self):
        custom_color = "#D04A5D"
        hover_color = "#B03B4A"

        # Botón Clientes
        clientes_button = ctk.CTkButton(
            self.main_frame,
            text="CLIENTES",
            width=200,
            height=50,
            fg_color=custom_color,
            hover_color=hover_color,
            font=("Comic Sans MS", 16, "bold"),  # Tamaño consistente con las otras interfaces
            command=lambda: [self.root.destroy(), Controlador.mostrar_clientes()]
        )
        clientes_button.pack(pady=10)

        # Botón Inventario
        inventario_button = ctk.CTkButton(
            self.main_frame,
            text="INVENTARIO",
            width=200,
            height=50,
            fg_color=custom_color,
            hover_color=hover_color,
            font=("Comic Sans MS", 16, "bold"),
            command=lambda: [self.root.destroy(), Controlador.mostrar_inventario()]
        )
        inventario_button.pack(pady=10)

        # Botón Ventas
        ventas_button = ctk.CTkButton(
            self.main_frame,
            text="VENTAS",
            width=200,
            height=50,
            fg_color=custom_color,
            hover_color=hover_color,
            font=("Comic Sans MS", 16, "bold"),
            command=lambda: [self.root.destroy(), Controlador.mostrar_ventas()]
        )
        ventas_button.pack(pady=10)

        # Botón Reportes
        reportes_button = ctk.CTkButton(
            self.main_frame,
            text="REPORTES",
            width=200,
            height=50,
            fg_color=custom_color,
            hover_color=hover_color,
            font=("Comic Sans MS", 16, "bold"),
            command=lambda: [self.root.destroy(), Controlador.mostrar_reportes()]
        )
        reportes_button.pack(pady=10)

# Ejecutar la aplicación principal
if __name__ == "__main__":
    MainApp()
