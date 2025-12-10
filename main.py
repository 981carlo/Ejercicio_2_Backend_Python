from fastapi import FastAPI, HTTPException, Request
from productos import ProductosAVL
from pedidos import PedidosNode, ListaEnlazadaPedidos


# RUTAS JSON
PRODUCTOS_JSON = "datos/productos.json"
PEDIDOS_JSON = "datos/pedidos.json"

app = FastAPI(
    title="API de Productos y Pedidos",
    description="Sistema con AVL para productos y lista enlazada para pedidos.",
    version="1.0"
)


# CARGA DE PRODUCTOS

productos_avl = ProductosAVL()
productos_avl.cargar_productos_json(PRODUCTOS_JSON)

# CARGAMOS LOS PRODUCTOS EN EL ÁRBOL SI NO EXIISTEN 
productos_iniciales = [
    {"id": 1, "nombre": "Teclado Mecánico RGB", "categoria": "Periféricos", "precio": 59.99},
    {"id": 2, "nombre": "Ratón Inalámbrico Logitech M185", "categoria": "Periféricos", "precio": 14.99},
    {"id": 3, "nombre": "Monitor 24'' Full HD", "categoria": "Monitores", "precio": 129.00},
    {"id": 4, "nombre": "Monitor 27'' 144Hz", "categoria": "Monitores", "precio": 249.00},
    {"id": 5, "nombre": "Auriculares Gaming HyperX Cloud II", "categoria": "Audio", "precio": 89.90},
    {"id": 6, "nombre": "Altavoces Logitech Z333", "categoria": "Audio", "precio": 49.99},
    {"id": 7, "nombre": "Disco SSD 500GB Samsung EVO", "categoria": "Almacenamiento", "precio": 68.50},
    {"id": 8, "nombre": "Disco HDD 1TB Seagate", "categoria": "Almacenamiento", "precio": 42.99},
    {"id": 9, "nombre": "Memoria RAM 16GB DDR4 3200MHz", "categoria": "Componentes", "precio": 72.90},
    {"id": 10, "nombre": "Procesador Intel i5-12400F", "categoria": "Componentes", "precio": 179.00},
    {"id": 11, "nombre": "Procesador AMD Ryzen 5 5600", "categoria": "Componentes", "precio": 159.00},
    {"id": 12, "nombre": "Placa Base MSI B550", "categoria": "Componentes", "precio": 118.00},
    {"id": 13, "nombre": "Fuente de Alimentación 650W 80+ Bronze", "categoria": "Componentes", "precio": 54.90},
    {"id": 14, "nombre": "Tarjeta Gráfica NVIDIA RTX 3060", "categoria": "Componentes", "precio": 329.00},
    {"id": 15, "nombre": "Cámara Web Full HD 1080p", "categoria": "Periféricos", "precio": 39.99},
    {"id": 16, "nombre": "Impresora Multifunción HP DeskJet 2720e", "categoria": "Oficina", "precio": 59.00},
    {"id": 17, "nombre": "Router WiFi 6 TP-Link AX1500", "categoria": "Redes", "precio": 79.99},
    {"id": 18, "nombre": "Switch Red 8 Puertos Gigabit", "categoria": "Redes", "precio": 32.90},
    {"id": 19, "nombre": "Silla Gaming Ergonómica", "categoria": "Mobiliario", "precio": 139.00},
    {"id": 20, "nombre": "Alfombrilla de Ratón XL", "categoria": "Periféricos", "precio": 12.50}
]

if not productos_avl.tree:
    for p in productos_iniciales:
        productos_avl.nuevo_producto(p["id"], p["nombre"], p["categoria"], p["precio"])
    productos_avl.guardar_productos_json(PRODUCTOS_JSON)


# CARGA DE PEDIDOS

lista_pedidos = ListaEnlazadaPedidos()
lista_pedidos.cargar_pedidos_json(PEDIDOS_JSON)



# ENDPOINTS PRODUCTOS

@app.post(
    "/productos/nuevo",
    summary="Crear un producto",
    description="Añade un nuevo producto al árbol AVL de productos."
)
async def nuevo_producto(id: int, request: Request):
    datos = await request.json()
    
    # VALIDAMOS LOS DAATOS OBLIGATORIOS    
    if "nombre" not in datos or "categoria" not in datos or "precio" not in datos:
        raise HTTPException(
            status_code=400,
            detail="Falta algún campo obligatorio: nombre, categoria, precio"
        )
    
    # VERIFICAMOS SI EL ID EXISTE   
    if productos_avl.get_producto(id) is not None:
        raise HTTPException(
            status_code=400,
            detail=f"El producto con id {id} ya existe"
        )
    
    productos_avl.nuevo_producto(
        id = id,
        nombre =datos["nombre"], 
        categoria = datos["categoria"], 
        precio = datos["precio"]
        )
    
    productos_avl.guardar_productos_json(PRODUCTOS_JSON)
    
    return {"mensaje": "Producto creado correctamente",
            "producto": {
                "id": id,
                "nombre": datos["nombre"],
                "categoria": datos["categoria"],
                "precio": datos["precio"]
            }}

@app.get(
    "/productos/listar",
    summary="Listar todos los productos",
    description="Devuelve todos los productos almacenados en el árbol AVL."
    )
async def listar_productos():
    return productos_avl.listar_productos()


@app.get(
    "/productos/{id}",
    summary="Obtener un producto",
    description="Devuelve la información de un producto identificado por su ID."
)
async def get_producto(id: int):
    producto = productos_avl.get_producto(id)
    return producto if producto else {"mensaje": "Producto no encontrado"}


# ENDPOINTS PEDIDOS

@app.post(
    "/pedidos/nuevo",
    summary="Crear un pedido",
    description="Crea un nuevo pedido indicando el cliente y una lista de IDs de productos separados por comas."
)
async def nuevo_pedido(request: Request):
    datos = await request.json()
        
    id_pedido = datos.get("id_pedido")
    cliente = datos.get("cliente")
    ids_productos = datos.get("productos_seleccionados",[])
    
    if id_pedido is None or cliente is None:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios: id_pedido, cliente")

    productos_seleccionados = []
    
    for pid in ids_productos:
        producto = productos_avl.get_producto(pid)
        if producto is None:
            raise HTTPException(status_code=404, detail=f"El producto con ID {pid} no existe")
        productos_seleccionados.append(producto)

    # CREAMOS NODO DEL PEDIDO
    nodo = PedidosNode(id_pedido, cliente, productos_seleccionados)
    
    # AGREGAMOS EL PEDIDO A LA LISTA ENLAZADA
    lista_pedidos.agregar_pedido(nodo)    
    
    # GUARDAMOS LOS PEDIDOS EN EL JSON
    lista_pedidos.guardar_pedidos_json(PEDIDOS_JSON)

    return {"mensaje": f"Pedido con ID {id_pedido} creado correctamente", "total": nodo.total}



@app.get(
    "/pedidos/listar",
    summary="Listar todos los pedidos",
    description="Devuelve todos los pedidos almacenados en la lista enlazada."
)
async def listar_pedidos():
    return lista_pedidos.listar_pedidos()



@app.get(
    "/pedidos/{id_pedido}",
    summary="Obtener un pedido",
    description="Devuelve los datos de un pedido especificado por su ID."
)
async def obtener_pedido(id_pedido: int):
    pedido = lista_pedidos.get_pedido(id_pedido)
    return {
        "id": pedido.id,
        "cliente": pedido.cliente,
        "productos_seleccionados": pedido.productos_seleccionados,
        "total": pedido.total
    } if pedido else {"mensaje": f"Pedido con ID {id_pedido} no existe"}



@app.put(
    "/pedidos/actualizar",
    summary="Actualizar un pedido",
    description="Permite actualizar el nombre del cliente y/o los productos del pedido."
)
async def actualizar_pedido(id_pedido: int, cliente: str = None, ids_productos: str = None):

    if cliente is None and ids_productos is None:
        return {"mensaje": "No se proporcionaron datos para actualizar el pedido"}

    nuevos_productos = None

    if ids_productos is not None:
        ids = [int(pid) for pid in ids_productos.split(",")]
        nuevos_productos = []
        for pid in ids:
            producto = productos_avl.get_producto(pid)
            if producto is None:
                return {"mensaje": f"El producto con ID {pid} no existe"}
            nuevos_productos.append(producto)

    pedido_actualizado = lista_pedidos.actualizar_pedido(
        id_pedido,
        cliente=cliente,
        nuevos_productos=nuevos_productos
    )

    if not pedido_actualizado:
        return {"error": f"Pedido con ID {id_pedido} no existe"}

    lista_pedidos.guardar_pedidos_json(PEDIDOS_JSON)
    return {"mensaje": f"Pedido con ID {id_pedido} actualizado correctamente"}



@app.delete(
    "/pedidos/borrar/{id_pedido}",
    summary="Borrar un pedido",
    description="Elimina un pedido de la lista enlazada usando su ID."
)
async def borrar_pedido(id_pedido: int):

    pedido_borrado = lista_pedidos.eliminar_pedido(id_pedido)

    if pedido_borrado:
        lista_pedidos.guardar_pedidos_json(PEDIDOS_JSON)
        return {"mensaje": f"Pedido con ID {id_pedido} eliminado correctamente"}

    return {"error": f"Pedido con ID {id_pedido} no existe"}
