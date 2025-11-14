// usuários simulados
const usuariosFake = [
    { usuario: "admin", senha: "123", tipo: "admin" },
    { usuario: "prof", senha: "123", tipo: "solicitante" }
];

document.getElementById("form-login").addEventListener("submit", function(e) {
    e.preventDefault();

    const user = document.getElementById("user").value.trim();
    const pass = document.getElementById("pass").value.trim();

    // validação
    if (!user || !pass) {
        alert("Preencha todos os campos!");
        return;
    }

    // busca usuário na lista fake
    const encontrado = usuariosFake.find(u => u.usuario === user && u.senha === pass);

    if (!encontrado) {
        alert("Usuário ou senha inválidos!");
        document.getElementById("pass").value = "";
        return;
    }

    // salva sessão local
    localStorage.setItem("usuarioLogado", encontrado.usuario);
    localStorage.setItem("tipoUsuario", encontrado.tipo);

    // redireciona
    if (encontrado.tipo === "admin") {
        window.location.href = "admin-dashboard.html";
    } else {
        window.location.href = "solicitante-dashboard.html";
    }
});
