let socket = null;
let produtos = [];

function conectar() {
    /* Evita abrir várias conexões */
    if (socket && socket.readyState === WebSocket.OPEN) {
        console.log("WebSocket já está conectado.");
        return;
    }
    console.log("Tentando conectar ao servidor...");

    socket = new WebSocket("ws://localhost:8888/ws");
    socket.onopen = function () {
        console.log("WebSocket conectado!");

        const status = document.getElementById("status");
        status.innerText = "Conectado";
        status.className = "conectado";
        document.getElementById("enviar").disabled = false;
    };

    socket.onclose = function () {
        console.log("WebSocket desconectado.");

        const status = document.getElementById("status");
        status.innerText = "Desconectado";
        status.className = "desconectado";
        document .getElementById("enviar").disabled = true;
    };

    socket.onerror = function (erro) {
        console.error("Erro no WebSocket:",erro);
    };

    socket.onmessage = function (evento) {
        try {
            const mensagem = JSON.parse(evento.data);

            console.log("Mensagem recebida:",mensagem);

            if (mensagem.acao === "produto_lido") {
                produtos = mensagem.produtos;
                atualizarTabela();
            }else if (mensagem.acao === "levantamento_completo") {
                alert("Levantamento enviado com sucesso!");
                produtos = [];
                atualizarTabela();
            }
        } catch (erro) {
            console.error("Erro ao processar mensagem:",erro);
        }
    };
}

function atualizarTabela() {
    const tabela = document.getElementById("tabela");

    tabela.innerHTML = "";

    if (produtos.length === 0) {
        tabela.innerHTML = `
            <tr>
                <td
                    colspan="3"
                    class="vazio"
                >
                    Nenhum produto registrado.
                </td>
            </tr>
        `;
        return;
    }

    produtos.forEach(item => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>
                ${item.produto.nome}
            </td>

            <td>
                ${item.produto.cod_barras}
            </td>

            <td>
                ${item.quantidade}
            </td>
            `;
        tabela.appendChild(linha);
    });

}

function enviarLevantamento() {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        alert("Servidor desconectado.");
        return;
    }

    if (produtos.length === 0) {
        alert("Nenhum produto foi registrado.");
        return;
    }

    const mensagem = { acao: "enviar_levantamento" };
    console.log("Enviando levantamento:",mensagem);
    socket.send(JSON.stringify(mensagem));
}

conectar();