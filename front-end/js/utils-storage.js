// esse salva uma nova solicitação
function salvarSolicitacao(solicitacao) {
    let lista = JSON.parse(localStorage.getItem("solicitacoes")) || [];
    lista.push(solicitacao);
    localStorage.setItem("solicitacoes", JSON.stringify(lista));
}

// esse carregar tudo pro admin
function carregarSolicitacoes() {
    return JSON.parse(localStorage.getItem("solicitacoes")) || [];
}

// e esse atualiza as solicitações
function atualizarSolicitacoes(lista) {
    localStorage.setItem("solicitacoes", JSON.stringify(lista));
}