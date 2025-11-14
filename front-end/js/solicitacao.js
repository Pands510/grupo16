if (localStorage.getItem("tipoUsuario") !== "solicitante") {
    window.location.href = "admin-dashboard.html";
}

document.addEventListener("DOMContentLoaded", () => {

    const btnSalvar = document.getElementById("salvar");
    const btnCancelar = document.getElementById("cancelar");
    const form = document.getElementById("form-solicitacao");

    btnSalvar.addEventListener("click", () => {
        if (!form.checkValidity()) {
            alert("Preencha todos os campos obrigatórios.");
            form.reportValidity();
            return;
        }

        const agora = new Date();
        const dataAbertura = agora.toLocaleString("pt-BR");

        const solicitacao = {
            nome: document.getElementById("nome").value,
            matricula: document.getElementById("matricula").value,
            cargo: document.getElementById("cargo").value,
            local: document.getElementById("local").value,
            descricao: document.getElementById("descricao").value,
            categoria: document.getElementById("categoria").value,
            dataAbertura: dataAbertura,
            protocolo: Math.floor(100000 + Math.random() * 900000),
            status: "Pendente"
        };

        salvarSolicitacao(solicitacao);

        alert("Solicitação salva com sucesso!");
        form.reset();
    });

    btnCancelar.addEventListener("click", () => {
        if (confirm("Deseja realmente cancelar?")) {
            form.reset();
        }
    });

});