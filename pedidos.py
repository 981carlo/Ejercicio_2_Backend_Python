import json
import os

class PedidosNode:
    def __init__(self, id_pedido, cliente, productos_seleccionados):
        self.id = id_pedido
        self.cliente = cliente
        self.productos_seleccionados = productos_seleccionados  
        self.total = sum(p["precio"] for p in productos_seleccionados)
        self.next = None

    
    def actualizar(self, cliente=None, productos_seleccionados=None):
        if cliente is not None:
            self.cliente = cliente

        if productos_seleccionados is not None:
            self.productos_seleccionados = productos_seleccionados
            self.total = sum(p["precio"] for p in productos_seleccionados)



class ListaEnlazadaPedidos:
    def __init__(self):
        self.head = None

    def agregar_pedido(self, pedido_node: PedidosNode):
        if self.head is None:
            self.head = pedido_node
        else:
            actual = self.head
            while actual.next is not None:
                actual = actual.next
            actual.next = pedido_node
            
    def actualizar_pedido(self, id_pedido, cliente=None, nuevos_productos=None):
        actual = self.head
        
        while actual:
            
            if actual.id == id_pedido:
                
                if cliente is not None:
                    actual.cliente = cliente
                
                if nuevos_productos is not None:
                    actual.productos_seleccionados = nuevos_productos
                    actual.total = sum(p["precio"] for p in nuevos_productos)                
                return True
            
            actual = actual.next    
    

    def get_pedido(self, id_pedido):
        actual = self.head
        while actual is not None:
            if actual.id == id_pedido:
                return actual
            actual = actual.next
        return None
    

    def eliminar_pedido(self, id_pedido: int):
        actual = self.head
        anterior = None

        while actual is not None:
            if actual.id == id_pedido:
                if anterior is None:
                    self.head = actual.next
                else:
                    anterior.next = actual.next                    
                return True
            
            anterior = actual
            actual = actual.next
        return False
    

    def listar_pedidos(self):
        pedidos = []
        actual = self.head
        while actual is not None:
            pedidos.append({
                "id": actual.id,
                "cliente": actual.cliente,
                "productos_seleccionados": actual.productos_seleccionados,
                "total": actual.total})
            actual = actual.next
        return pedidos
    
    
    def pedidos_a_json(self):
        return json.dumps(self.listar_pedidos())
    

    def guardar_pedidos_json(self, ruta_archivo):
        datos = []
        actual = self.head
        
        while actual:
            datos.append({
                "id": actual.id,
                "cliente": actual.cliente,
                "productos_seleccionados": actual.productos_seleccionados,
                "total": actual.total
            })
            actual = actual.next
            
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
            
    
    def cargar_pedidos_json(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return "No se encuentra el archivo"
        
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
            for pedido in datos:
                nodo = PedidosNode(
                    id_pedido = pedido["id"],
                    cliente = pedido["cliente"],
                    productos_seleccionados = pedido["productos_seleccionados"]
                )
                self.agregar_pedido(nodo)