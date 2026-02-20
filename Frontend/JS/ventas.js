// 🔐 PROTECCIÓN
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    cargarVentas();

    document
        .getElementById("form-venta")
        .addEventListener("submit", registrarVenta);
});

// 📦 Cargar productos en select
function cargarProductos() {
    fetch("http://127.0.0.1:5000/productos")
        .then(res => res.json())
        .then(data => {
            const select = document.getElementById("producto");
            select.innerHTML = "";

            data.forEach(p => {
                const option = document.createElement("option");
                option.value = p.id;
                option.textContent = `${p.nombre} (Stock: ${p.stock})`;
                select.appendChild(option);
            });
        });
}

// 🧾 Registrar venta
function registrarVenta(e) {
    e.preventDefault();

    const venta = {
        producto_id: document.getElementById("producto").value,
        cantidad: document.getElementById("cantidad").value
    };

    fetch("http://127.0.0.1:5000/ventas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(venta)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("mensaje").innerText = data.mensaje;
        e.target.reset();

        cargarVentas();
        cargarProductos(); // actualizar stock visible
    })
    .catch(err => console.error("Error:", err));
}

// 📊 Mostrar historial
function cargarVentas() {
    fetch("http://127.0.0.1:5000/ventas")
        .then(res => res.json())
        .then(data => {
            const tabla = document.getElementById("tabla-ventas");
            tabla.innerHTML = "";

            data.forEach(v => {
                const fila = document.createElement("tr");

                const fecha = new Date(v.fecha)
                    .toLocaleString("es-PE");

                fila.innerHTML = `
                    <td>${v.id}</td>
                    <td>${v.producto}</td>
                    <td>${v.cantidad}</td>
                    <td>${fecha}</td>
                `;

                tabla.appendChild(fila);
            });
        });
}

// 🔓 Logout
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
