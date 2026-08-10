(function () {
    const CHAVE_ARMAZENAMENTO = "painel-tarefas:modo-escuro";
    const corpo = document.body;
    const botao = document.getElementById("botao-modo-escuro");

    function aplicarModo(ativo) {
        corpo.classList.toggle("modo-escuro", ativo);
        corpo.classList.toggle("bg-dark", ativo);
        corpo.classList.toggle("text-light", ativo);
        if (botao) {
            const icone = botao.querySelector("i");
            icone.className = ativo ? "bi bi-sun" : "bi bi-moon-stars";
        }
    }

    const preferenciaSalva = localStorage.getItem(CHAVE_ARMAZENAMENTO) === "true";
    aplicarModo(preferenciaSalva);

    if (botao) {
        botao.addEventListener("click", function () {
            const ativoAgora = !corpo.classList.contains("modo-escuro");
            aplicarModo(ativoAgora);
            localStorage.setItem(CHAVE_ARMAZENAMENTO, ativoAgora);
        });
    }
})();
