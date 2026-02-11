// 🔐 SOLO ADMIN
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

if (usuario.rol !== "admin") {
    alert("Solo administradores");
    window.location.href = "productos.html";
}

document.addEventListener("DOMContentLoaded", () => {
    fetch("http://127.0.0.1:5000/usuarios")
        .then(res => res.json())
        .then(data => {
            const tabla = document.getElementById("tabla-usuarios");
            tabla.innerHTML = "";

            data.forEach(u => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${u.id}</td>
                    <td>${u.nombre}</td>
                    <td>${u.correo}</td>
                    <td>${u.rol}</td>
                `;
                tabla.appendChild(fila);
            });
        });
});

function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
