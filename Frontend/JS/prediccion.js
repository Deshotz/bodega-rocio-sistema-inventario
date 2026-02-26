const usuario = JSON.parse(localStorage.getItem("usuario"));

if (!usuario) {
    window.location.href = "index.html";
}

let grafica = null;

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
        });
});

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

            const fechas = [];
            const valores = [];

            data.predicciones.forEach(item => {
                fechas.push(item.fecha);
                valores.push(item.demanda_predicha);
            });

            const demandaTotal = valores.reduce((a,b)=>a+b,0);

            document.getElementById("resumenDemanda").innerHTML = `
                📦 Producto: <b>${data.producto}</b><br>
                📊 Tipo: ${data.tipo_producto}<br>
                🔠 Clasificación ABC: ${data.clasificacion_abc}<br>
                🚨 Criticidad: <b>${data.nivel_criticidad}</b><br>
                ⏳ Lead Time: ${data.lead_time} días<br><br>
                🔮 Demanda estimada (${dias} días): 
                <b>${demandaTotal.toFixed(2)} unidades</b>
            `;

            const ctx = document.getElementById("graficaPrediccion").getContext("2d");

            if (grafica) grafica.destroy();

            grafica = new Chart(ctx, {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Demanda Predicha",
                        data: valores,
                        borderColor: "#8e44ad",
                        backgroundColor: "rgba(142,68,173,0.2)",
                        borderWidth: 3,
                        tension: 0.3,
                        fill: true
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

function reabastecer() {

    const producto_id = document.getElementById("producto").value;

    fetch(`http://127.0.0.1:5000/ia/reabastecimiento/${producto_id}`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            let color = "green";

            if (data.nivel_criticidad === "Crítico") color = "red";
            else if (data.nivel_criticidad === "Alto") color = "orange";
            else if (data.nivel_criticidad === "Medio") color = "#f1c40f";

            document.getElementById("resultado-reabastecimiento").innerHTML = `
                📊 Demanda estimada (Lead Time ${data.lead_time} días): 
                ${data.demanda_estimada} unidades <br>
                📦 Stock actual: ${data.stock_actual} unidades <br><br>
                🛒 <span class="alerta-compra" style="color:${color};">
                Comprar: ${data.recomendacion_compra} unidades
                </span>
            `;
        });
}

function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}