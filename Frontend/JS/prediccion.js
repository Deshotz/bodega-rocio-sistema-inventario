// =========================
// PROTECCIÓN DE SESIÓN
// =========================
const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}


// =========================
// CARGAR PRODUCTOS
// =========================
document.addEventListener("DOMContentLoaded", () => {

    fetch("http://127.0.0.1:5000/productos")
        .then(res => res.json())
        .then(data => {

            const select = document.getElementById("producto");

            data.forEach(p => {
                const option = document.createElement("option");
                option.value = p.id;
                option.textContent = p.nombre;
                select.appendChild(option);
            });
        })
        .catch(() => {
            alert("Error al cargar productos");
        });
});


// =========================
// GRÁFICA GLOBAL
// =========================
let grafica = null;


// =========================
// PREDICCIÓN
// =========================
function predecir() {

    const producto_id = document.getElementById("producto").value;
    const dias = document.getElementById("dias").value;

    fetch(`http://127.0.0.1:5000/ia/prediccion/${producto_id}?dias=${dias}`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            const tabla = document.getElementById("tabla-prediccion");
            tabla.innerHTML = "";

            const fechas = [];
            const valores = [];

            data.forEach(item => {

                const fila = document.createElement("tr");

                fila.innerHTML = `
                    <td>${item.fecha}</td>
                    <td>${item.demanda_predicha}</td>
                `;

                tabla.appendChild(fila);

                fechas.push(item.fecha);
                valores.push(item.demanda_predicha);
            });

            // ===== CREAR GRÁFICA =====

            const ctx = document.getElementById("graficaPrediccion").getContext("2d");

            if (grafica) grafica.destroy();

            grafica = new Chart(ctx, {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Demanda Predicha",
                        data: valores,
                        borderWidth: 3,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "Unidades"
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: "Fecha"
                            }
                        }
                    }
                }
            });
        })
        .catch(() => {
            alert("Error al obtener la predicción");
        });
}


// =========================
// REABASTECIMIENTO
// =========================
function reabastecer() {

    const producto_id = document.getElementById("producto").value;
    const dias = document.getElementById("dias").value;

    fetch(`http://127.0.0.1:5000/ia/reabastecimiento/${producto_id}?dias=${dias}`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            const texto = `
                📊 Demanda estimada: ${data.demanda_estimada} unidades <br>
                📦 Stock actual: ${data.stock_actual} unidades <br>
                🛒 <span style="color:red;">Comprar: ${data.recomendacion_compra} unidades</span>
            `;

            document.getElementById("resultado-reabastecimiento").innerHTML = texto;
        })
        .catch(() => {
            alert("Error al calcular reabastecimiento");
        });
}


// =========================
// LOGOUT
// =========================
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
