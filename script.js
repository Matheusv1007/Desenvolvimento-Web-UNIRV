const botaoTema = document.getElementById("btnTema");
const pagina = document.documentElement;

function atualizarTextoBotao() {
    const temaAtual = pagina.getAttribute("data-bs-theme");

    if (temaAtual === "dark") {
        botaoTema.textContent = "Modo Claro";
    } else {
        botaoTema.textContent = "Modo Noturno";
    }
}

const temaSalvo = localStorage.getItem("tema");

if (temaSalvo) {
    pagina.setAttribute("data-bs-theme", temaSalvo);
    atualizarTextoBotao();
}

botaoTema.addEventListener("click", function () {
    const temaAtual = pagina.getAttribute("data-bs-theme");

    if (temaAtual === "dark") {
        pagina.setAttribute("data-bs-theme", "light");
        localStorage.setItem("tema", "light");
    } else {
        pagina.setAttribute("data-bs-theme", "dark");
        localStorage.setItem("tema", "dark");
    }

    atualizarTextoBotao();
});
