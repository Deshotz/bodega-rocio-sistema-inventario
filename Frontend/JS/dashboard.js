const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}


// ==========================
// CARGAR KPIs
// ==========================
function cargarKPIs() {

    // 📊 KPIs básicos
    fetch("http://127.0.0.1:5000/dashboard/kpis")
        .then(res => res.json())
        .then(data => {

            document.getElementById("ventasTotales").textContent =
                data.ventas_totales + " ventas";

            document.getElementById("stockBajo").textContent =
                data.stock_bajo + " productos";

            document.getElementById("productoTop").textContent =
                data.producto_top;
        });

    // 🤖 COMPRA IA GLOBAL
    fetch("http://127.0.0.1:5000/ia/recomendacion-global?dias=7")
        .then(res => res.json())
        .then(data => {

            document.getElementById("compraIA").textContent =
                data.recomendacion_compra + " unidades";
        });
}


// ==========================
// GRÁFICA DE VENTAS
// ==========================
let grafica = null;

function cargarGrafica() {

    fetch("http://127.0.0.1:5000/dashboard/ventas")
        .then(res => res.json())
        .then(data => {

            const fechas = data.map(d => d.fecha);
            const valores = data.map(d => d.total);

            const ctx = document.getElementById("graficaVentas").getContext("2d");

            grafica = new Chart(ctx, {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Ventas",
                        data: valores,
                        borderWidth: 3,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        });
}


// ==========================
// INICIO
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    cargarKPIs();
    cargarGrafica();
});


// ==========================
// LOGOUT
// ==========================
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
