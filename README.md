# 🏪 Sistema de Gestión de Inventarios - Bodega Rocío

Proyecto académico desarrollado para la implementación de un sistema web de gestión básica de inventarios utilizando arquitectura MVC con Flask y MySQL.

---

## 📌 Descripción General

El Sistema de Gestión de Inventarios – Bodega Rocío es una aplicación web que permite administrar productos, controlar el stock, visualizar movimientos de inventario, gestionar usuarios y generar alertas automáticas por stock bajo.

El proyecto fue desarrollado siguiendo metodología ágil SCRUM, implementando las historias de usuario definidas para el Sprint 1 (PMV 1).

---

## 🎯 Objetivo del Sprint 1

Implementar las funcionalidades mínimas necesarias para el control básico del inventario, permitiendo:

- Registrar productos
- Actualizar stock (+ / -)
- Visualizar inventario
- Generar alertas por stock bajo
- Gestionar usuarios
- Implementar autenticación y control de roles

---

## 🚀 Tecnologías Utilizadas

### 🔹 Backend
- Python 3
- Flask
- Flask-CORS
- MySQL
- Arquitectura MVC

### 🔹 Frontend
- HTML5
- CSS3
- JavaScript (Vanilla JS)
- LocalStorage para manejo de sesión

---

## 📂 Estructura del Proyecto

```
TP-BR/
│
├── Backend/
│   ├── Controlador/
│   │   ├── producto_controller.py
│   │   ├── inventario_controller.py
│   │   └── usuario_controller.py
│   │
│   ├── Modelo/
│   │   ├── producto_model.py
│   │   ├── inventario_model.py
│   │   ├── usuario_model.py
│   │   └── db.py
│   │
│   ├── app.py
│   └── config.py
│
├── Frontend/
│   ├── CSS/
│   │   └── styles.css
│   │
│   ├── JS/
│   │   ├── app.js
│   │   ├── inventario.js
│   │   ├── usuarios.js
│   │   └── index.js
│   │
│   └── Vista/
│       ├── index.html
│       ├── productos.html
│       ├── inventario.html
│       └── usuarios.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 👥 Roles del Sistema

### 👑 Administrador
- Registrar productos
- Actualizar stock
- Eliminar productos
- Ver alertas de stock bajo
- Gestionar usuarios
- Acceso completo al sistema

### 👤 Usuario
- Visualizar movimientos de inventario
- Acceso limitado según rol

---

## 🔐 Seguridad Implementada

- Autenticación mediante validación de credenciales en backend
- Control de acceso por rol (admin / usuario)
- Protección de vistas mediante verificación en frontend
- Manejo de sesión usando LocalStorage

---

## 📦 Funcionalidades Implementadas (Sprint 1)

✔ HU01 – Registrar productos  
✔ HU02 – Actualizar stock  
✔ HU03 – Visualizar inventario  
✔ HU04 – Alertas automáticas por stock bajo  
✔ HU05 – Gestión básica de usuarios  
✔ Autenticación de usuarios  
✔ Control de roles  

---

## 🛠 Instalación y Configuración

### 1️⃣ Clonar el repositorio

```
git clone https://github.com/TU_USUARIO/bodega-rocio-sistema-inventario.git
```

### 2️⃣ Crear entorno virtual

```
python -m venv venv
```

Activar entorno (Windows):

```
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```
pip install -r requirements.txt
```

### 4️⃣ Configurar Base de Datos

Crear base de datos en MySQL:

```
CREATE DATABASE bodega_rocio;
```

Configurar credenciales en `config.py`.

---

## ▶️ Ejecutar el Sistema

Desde la carpeta Backend:

```
python app.py
```

Servidor disponible en:

```
http://127.0.0.1:5000
```

Abrir frontend desde:

```
Frontend/Vista/index.html
```

---

## 📊 Próxima Fase (Sprint 2)

- Implementación de predicción básica de demanda
- Análisis de datos históricos
- Visualización de gráficos
- Integración de Inteligencia Artificial básica

---

## 👨‍💻 Autor

Reynaldo Elías Cajamarca Areche  
Ingeniería de Sistemas e Informática  
Universidad Continental  
2026
