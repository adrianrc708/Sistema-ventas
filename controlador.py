from vista_clientes import CRUDclientes
from vista_inventario import CRUDproductos
from vista_ventas import CRUDventas
from vista_reportes import CRUDReportes

class Controlador:
    @staticmethod
    def mostrar_menu_principal():
        from main import MainApp  # Importación diferida para evitar importaciones circulares
        MainApp()

    @staticmethod
    def mostrar_clientes():
        CRUDclientes().crud()

    @staticmethod
    def mostrar_inventario():
        CRUDproductos().crud()

    @staticmethod
    def mostrar_ventas():
        CRUDventas().crud()
    
    @staticmethod
    def mostrar_reportes():
        CRUDReportes().crud()
