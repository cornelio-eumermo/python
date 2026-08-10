(function () {
    const listaTarefas = document.getElementById("lista-tarefas");
    const rotuloFiltro = document.getElementById("rotulo-filtro");
    const itensFiltro = document.querySelectorAll(".item-filtro");

    const CLASSES_STATUS = {
        "pendente": "status-pendente",
        "em andamento": "status-em-andamento",
        "concluida": "status-concluida",
    };

    function criarCardTarefa(tarefa) {
        const coluna = document.createElement("div");
        coluna.className = "col-12 col-md-6 col-lg-4";

        const classeStatus = CLASSES_STATUS[tarefa.status] || "";

        coluna.innerHTML = `
            <div class="card card-tarefa ${classeStatus} h-100 shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="card-title"></h5>
                        <span class="badge rounded-pill badge-status"></span>
                    </div>
                    <p class="card-text"></p>
                    <div class="d-flex gap-2">
                        <a class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-pencil-square"></i> Editar
                        </a>
                        <form method="POST">
                            <button type="submit" class="btn btn-sm btn-outline-danger">
                                <i class="bi bi-trash"></i> Excluir
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        `;

        coluna.querySelector(".card-title").textContent = tarefa.titulo;
        coluna.querySelector(".badge-status").textContent = tarefa.status;
        coluna.querySelector(".card-text").textContent = tarefa.descricao || "Sem descrição.";
        coluna.querySelector("a.btn-outline-primary").href = `/editar/${tarefa.id}`;
        coluna.querySelector("form").action = `/excluir/${tarefa.id}`;

        return coluna;
    }

    function renderizarTarefas(tarefas) {
        listaTarefas.innerHTML = "";

        if (tarefas.length === 0) {
            listaTarefas.innerHTML = `
                <div class="col-12">
                    <p class="text-secondary text-center py-5">Nenhuma tarefa encontrada.</p>
                </div>`;
            return;
        }

        tarefas.forEach((tarefa) => listaTarefas.appendChild(criarCardTarefa(tarefa)));
    }

    async function filtrarPorStatus(status, rotulo) {
        try {
            const parametros = status ? `?status=${encodeURIComponent(status)}` : "";
            const resposta = await fetch(`/api/tarefas${parametros}`);
            const tarefas = await resposta.json();
            renderizarTarefas(tarefas);
            if (rotuloFiltro) rotuloFiltro.textContent = rotulo;
        } catch (erro) {
            console.error(erro);
        }
    }

    itensFiltro.forEach((item) => {
        item.addEventListener("click", (evento) => {
            evento.preventDefault();
            filtrarPorStatus(item.dataset.status, item.textContent.trim());
        });
    });
})();
