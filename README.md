# API de Gestión de Productos y Pedidos  
### (Árbol AVL + Lista Enlazada + FastAPI)

Este proyecto implementa una API REST para gestionar **productos** y **pedidos**, utilizando estructuras de datos avanzadas en Python:

- **Productos** almacenados en un **árbol AVL** (`bintrees.AVLTree`)
- **Pedidos** almacenados en una **lista enlazada propia**
- **Persistencia** en archivos JSON
- **API REST** implementada con **FastAPI**

---

## 🧱 Tecnologías utilizadas

- Python 3.x (no funciona con Python 3.10 y superiores)
- FastAPI
- Uvicorn
- bintrees (AVLTree)
- Estructuras de datos creadas manualmente:
  - Árbol AVL
  - Lista enlazada simple

---

## 🚀 Cómo ejecutar el proyecto

Instala las dependencias:

```bash
pip install fastapi uvicorn bintrees
```

Ejecuta el servidor:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

---

## 📂 Documentación automática

FastAPI proporciona documentación interactiva:

🔗 **Swagger UI**  
http://127.0.0.1:8000/docs

🔗 **ReDoc**  
http://127.0.0.1:8000/redoc

---

## 🗂 Endpoints principales

### 🔹 Productos

| Método | Ruta | Descripción |
|--------|-------|-------------|
| POST | `/productos/nuevo` | Crear un producto |
| GET  | `/productos/listar` | Listar productos |
| GET  | `/productos/{id}`   | Obtener producto por ID |

---

### 🔹 Pedidos

| Método | Ruta | Descripción |
|--------|-------|-------------|
| POST   | `/pedidos/nuevo`                     | Crear un pedido |
| GET    | `/pedidos/listar`                    | Listar pedidos |
| GET    | `/pedidos/{id}`                      | Obtener pedido por ID |
| PUT    | `/pedidos/actualizar?id_pedido={id}` | Actualizar un pedido |
| DELETE | `/pedidos/borrar/{id}`               | Eliminar un pedido |

---

## 💾 Persistencia

Los datos se guardan automáticamente en formato JSON:

- `datos/productos.json`
- `datos/pedidos.json`

Esto permite reiniciar el servidor sin perder información.

---

## 👤 Autor

Proyecto realizado por **[Carlo García González]**.

