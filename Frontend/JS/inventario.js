// 🔐 PROTECCIÓN
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
    fetch("http://127.0.0.1:5000/inventario")
        .then(res => res.json())
        .then(data => {
            const tabla = document.getElementById("tabla-inventario");
            tabla.innerHTML = "";

            data.forEach(item => {
                const fila = document.createElement("tr");
                const fecha = new Date(item.fecha).toLocaleString("es-PE");

                fila.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.producto}</td>
                    <td>${item.cantidad}</td>
                    <td>${fecha}</td>
                `;
                tabla.appendChild(fila);
            });
        });
});

function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
