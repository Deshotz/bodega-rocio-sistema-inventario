document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-login");
    form.addEventListener("submit", login);
});

function login(e) {
    e.preventDefault();

    const datos = {
        correo: document.getElementById("correo").value,
        password: document.getElementById("password").value
    };

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("mensaje").innerText = data.error;
        } else {
            localStorage.setItem("usuario", JSON.stringify(data));

            if (data.rol === "admin") {
                window.location.href = "productos.html";
            } else {
                window.location.href = "inventario.html";
            }
        }
    })
    .catch(err => console.error("Error en login:", err));
}
