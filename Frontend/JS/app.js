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

                // 🔥 COLOR SEGÚN CRITICIDAD
                if (producto.nivel_criticidad === "Crítico") {
                    fila.classList.add("fila-critico");
                }
                else if (producto.nivel_criticidad === "Alto") {
                    fila.classList.add("fila-alto");
                }
                else if (producto.nivel_criticidad === "Medio") {
                    fila.classList.add("fila-medio");
                }

                // 🔔 ALERTA STOCK BAJO
                if (producto.stock <= 5) {
                    const alerta = document.createElement("div");
                    alerta.className = "alerta";
                    alerta.innerText = `⚠️ Stock bajo: ${producto.nombre} (${producto.stock} unidades)`;
                    alertas.appendChild(alerta);
                }

                // 🎨 BADGE SEGÚN CRITICIDAD
                let claseBadge = "";
                if (producto.nivel_criticidad === "Crítico") claseBadge = "critico";
                else if (producto.nivel_criticidad === "Alto") claseBadge = "alto";
                else if (producto.nivel_criticidad === "Medio") claseBadge = "medio";
                else claseBadge = "bajo";

                fila.innerHTML = `
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>${producto.categoria}</td>
                    <td>S/ ${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.tipo_producto}</td>
                    <td>${producto.clasificacion_abc}</td>
                    <td>
                        <span class="badge ${claseBadge}">
                            ${producto.nivel_criticidad}
                        </span>
                    </td>
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

function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}