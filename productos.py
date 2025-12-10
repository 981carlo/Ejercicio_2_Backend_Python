import json
import os
from bintrees import AVLTree

class ProductosAVL:
    def __init__(self):        
        self.tree = AVLTree()

    # FUNCIÓN PARA AGREGAR PRODUCTOS 
    def nuevo_producto(self, id: int, nombre: str, categoria: str, precio: float):
        
        producto = {
            "id": id,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio
        }
        # INSERTAMOS PRODUCTO CON LA CLAVE id
        self.tree.insert(id, producto)

    def get_producto(self, id:int):
        try:
            return self.tree[id]
        except KeyError:
            return None 
        
    def listar_productos(self):
        return [value for _, value in self.tree.items()]
        
        
    def guardar_productos_json(self, ruta_archivo):
        
        productos = list(self.tree.values())
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
            
    
    def cargar_productos_json(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return "Archivo no encontrado"
        
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            productos = json.load(f)
            
            for p in productos:
                self.tree.insert(p["id"], p)
