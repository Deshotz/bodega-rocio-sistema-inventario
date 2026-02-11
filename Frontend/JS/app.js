// 🔐 PROTECCIÓN (solo admin)
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

if (usuario.rol !== "admin") {
    alert("Acceso denegado");
    window.location.href = "inventario.html";
}

document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    document.getElementById("form-producto")
        .addEventListener("submit", registrarProducto);
});

// HU03 + HU04
function cargarProductos() {
    fetch("http://127.0.0.1:5000/productos")
        .then(res => res.json())
        .then(data => {
            const tabla = document.getElementById("tabla-productos");
            const alertas = document.getElementById("alertas-stock");

            tabla.innerHTML = "";
            alertas.innerHTML = "";

            data.forEach(producto => {
                const fila = document.createElement("tr");

                if (producto.stock <= 5) {
                    fila.classList.add("stock-bajo");

                    const alerta = document.createElement("div");
                    alerta.className = "alerta";
                    alerta.innerText = `⚠️ Stock bajo: ${producto.nombre} (${producto.stock} unidades)`;
                    alertas.appendChild(alerta);
                }

                fila.innerHTML = `
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>${producto.categoria}</td>
                    <td>${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>
                        <button onclick="actualizarStock(${producto.id}, 1)">➕</button>
                        <button onclick="actualizarStock(${producto.id}, -1)">➖</button>
                        <button onclick="eliminarProducto(${producto.id})">🗑</button>
                    </td>
                `;

                tabla.appendChild(fila);
            });
        });
}

// HU01
function registrarProducto(e) {
    e.preventDefault();

    const producto = {
        nombre: nombre.value,
        categoria: categoria.value,
        precio: precio.value,
        stock: stock.value
    };

    fetch("http://127.0.0.1:5000/productos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(producto)
    })
    .then(res => res.json())
    .then(data => {
        mensaje.innerText = data.mensaje;
        e.target.reset();
        cargarProductos();
    });
}

// HU02
function actualizarStock(id, cantidad) {
    fetch(`http://127.0.0.1:5000/productos/${id}/stock`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cantidad })
    })
    .then(() => cargarProductos());
}

function eliminarProducto(id) {
    if (!confirm("¿Eliminar producto?")) return;

    fetch(`http://127.0.0.1:5000/productos/${id}`, {
        method: "DELETE"
    })
    .then(() => cargarProductos());
}

// 🔓 LOGOUT
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
