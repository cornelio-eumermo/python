(function () {
    const ROTULOS = ["Pendente", "Em andamento", "Concluída"];
    const CHAVES = ["pendente", "em andamento", "concluida"];
    const CORES = ["#f1c40f", "#3498db", "#2ecc71"];

    async function carregarProgresso() {
        try {
            const resposta = await fetch("/api/progresso");
            const contagem = await resposta.json();
            const valores = CHAVES.map((chave) => contagem[chave] || 0);
            desenharGraficos(valores);
        } catch (erro) {
            console.error(erro);
        }
    }

    function desenharGraficos(valores) {
        const ctxBarras = document.getElementById("grafico-barras");
        const ctxPizza = document.getElementById("grafico-pizza");

        new Chart(ctxBarras, {
            type: "bar",
            data: {
                labels: ROTULOS,
                datasets: [{
                    label: "Tarefas",
                    data: valores,
                    backgroundColor: CORES,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });

        new Chart(ctxPizza, {
            type: "pie",
            data: {
                labels: ROTULOS,
                datasets: [{
                    data: valores,
                    backgroundColor: CORES,
                }],
            },
            options: { responsive: true },
        });
    }

    carregarProgresso();
})();
