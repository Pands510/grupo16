// --- controle de acesso ---
if (!localStorage.getItem("usuarioLogado")) {
    window.location.href = "login.html";
}

if (localStorage.getItem("tipoUsuario") !== "admin") {
    window.location.href = "solicitante-dashboard.html";
}

document.addEventListener("DOMContentLoaded", () => {
    mostrarSolicitacoes();
});

// --- função principal de exibição ---
function mostrarSolicitacoes(listaPersonalizada = null) {
    const area = document.getElementById("lista-solicitacoes");
    const lista = listaPersonalizada || carregarSolicitacoes();

    if (lista.length === 0) {
        area.innerHTML = "<p>Nenhuma solicitação cadastrada.</p>";
        return;
    }

    let html = `
        <table border='1' cellpadding='6'>
        <tr>
            <th>Protocolo</th>
            <th>Solicitante</th>
            <th>Local</th>
            <th>Categoria</th>
            <th>Data</th>
            <th>Status</th>
            <th>Ações</th>
        </tr>
    `;

    lista.forEach((s, index) => {
        html += `
            <tr>
                <td>${s.protocolo}</td>
                <td>${s.nome}</td>
                <td>${s.local}</td>
                <td>${s.categoria}</td>
                <td>${s.dataAbertura}</td>
                <td>
                    <select onchange="alterarStatus(${index}, this.value)">
                        <option ${s.status === "Pendente" ? "selected" : ""}>Pendente</option>
                        <option ${s.status === "Em andamento" ? "selected" : ""}>Em andamento</option>
                        <option ${s.status === "Aprovada" ? "selected" : ""}>Aprovada</option>
                        <option ${s.status === "Negada" ? "selected" : ""}>Negada</option>
                    </select>
                </td>
                <td>
                    <button onclick="detalhes(${index})">Ver detalhes</button>
                </td>
            </tr>
        `;
    });

    html += "</table>";
    area.innerHTML = html;
}

// --- alterar status ---
function alterarStatus(index, novoStatus) {
    let lista = carregarSolicitacoes();
    lista[index].status = novoStatus;
    atualizarSolicitacoes(lista);

    alert("Status alterado!");
}

// --- ver detalhes ---
function detalhes(index) {
    const s = carregarSolicitacoes()[index];

    alert(`
Detalhes da solicitação

Solicitante: ${s.nome}
Matrícula: ${s.matricula}
Cargo: ${s.cargo}
Local: ${s.local}

Descrição:
${s.descricao}

Categoria: ${s.categoria}
Data: ${s.dataAbertura}
Status: ${s.status}
    `);
}

// --- filtrar categoria ---
function filtrarPorCategoria(cat) {
    const lista = carregarSolicitacoes();
    const filtrada = lista.filter(s => s.categoria === cat);
    mostrarSolicitacoes(filtrada);
}