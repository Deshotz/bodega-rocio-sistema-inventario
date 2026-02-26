const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

let grafica = null;

function cargarKPIs() {

    fetch("http://127.0.0.1:5000/dashboard/kpis")
        .then(res => res.json())
        .then(data => {

            document.getElementById("ventasTotales").textContent =
                data.ventas_totales + " ventas";

            document.getElementById("stockBajo").textContent =
                data.stock_bajo + " productos";

            document.getElementById("productoTop").textContent =
                data.producto_top;

            document.getElementById("productosCriticos").textContent =
                data.productos_criticos;

            document.getElementById("productosA").textContent =
                data.productos_a;
        });
}

function cargarGrafica() {

    fetch("http://127.0.0.1:5000/dashboard/ventas")
        .then(res => res.json())
        .then(data => {

            const fechas = data.map(d => d.fecha);
            const valores = data.map(d => d.total);

            const ctx = document.getElementById("graficaVentas").getContext("2d");

            if (grafica) grafica.destroy();

            grafica = new Chart(ctx, {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Ventas",
                        data: valores,
                        borderColor: "#3498db",
                        backgroundColor: "rgba(52,152,219,0.2)",
                        borderWidth: 3,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        });
}

document.addEventListener("DOMContentLoaded", () => {
    cargarKPIs();
    cargarGrafica();
});

function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}