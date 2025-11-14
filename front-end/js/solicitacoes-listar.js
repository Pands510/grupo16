document.addEventListener("DOMContentLoaded", () => {
    const area = document.getElementById("lista-solicitacoes");
    const lista = carregarSolicitacoes();

    if (lista.length === 0) {
        area.innerHTML = "<p>Nenhuma solicitação enviada ainda.</p>";
        return;
    }

    let html = "<ul>";

    lista.forEach(s => {
        html += `
            <li>
                <strong>Protocolo:</strong> ${s.protocolo}<br>
                <strong>Local:</strong> ${s.local}<br>
                <strong>Data:</strong> ${s.dataAbertura}<br>
                <strong>Status:</strong> ${s.status}
            </li><br>
        `;
    });

    html += "</ul>";
    area.innerHTML = html;
});
