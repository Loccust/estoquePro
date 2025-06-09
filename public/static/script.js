// Função para exibir o formulário de adição de itens
function showAddForm() {
    // Obtém o container de formulários
    const formContainer = document.getElementById('form-container');
  
    // Insere o HTML do formulário de adição
    formContainer.innerHTML = `
        <h2>Adicionar Item</h2>
        <form id="addForm">
            <input type="text" id="codigo" placeholder="Código do Produto" required>
            <input type="text" id="nome" placeholder="Nome do Item" required>
            <input type="number" id="quantidade" placeholder="Quantidade" required>
            <input type="number" id="saida" placeholder="Quantidade de Saída" required>
            <input type="date" id="data" required>
            <input type="text" id="setor" placeholder="Setor" required>
            <button type="submit">Adicionar</button>
        </form>
    `;
  
    // Adiciona o event listener para o submit do formulário
    document.getElementById('addForm').addEventListener('submit', function (e) {
        e.preventDefault(); // Impede o comportamento padrão de recarregar a página
  
        // Obtém e valida os valores dos campos
        let codigo = document.getElementById('codigo').value.trim();
        if (!codigo) {
            alert("O código do item é obrigatório!");
            return;
        }
  
        let nome = document.getElementById('nome').value.trim();
        let quantidade = parseInt(document.getElementById('quantidade').value);
        let saida = parseInt(document.getElementById('saida').value);
        let data = document.getElementById('data').value.trim();
        let setor = document.getElementById('setor').value.trim();
  
        // Cria o objeto do novo item
        const novoItem = { 
            codigo, 
            nome, 
            quantidade, 
            saida, 
            quantidadeAposSaida: quantidade - saida, // Calcula a quantidade após saída
            data, 
            setor 
        };
  
        // Envia a requisição POST para a API
        fetch('/api/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(novoItem),
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('Item adicionado:', data);
            viewInventory(); // Atualiza a exibição do inventário
            formContainer.innerHTML = ''; // Limpa o formulário
        })
        .catch((err) => console.error('Erro ao adicionar item:', err));
    });
}
  
// Função para exibir o formulário de atualização de itens
function showUpdateForm() {
    const formContainer = document.getElementById('form-container');
  
    formContainer.innerHTML = `
        <h2>Atualizar Item</h2>
        <form id="updateForm">
            <input type="text" id="codigo" placeholder="Código do Produto" required>
            <input type="number" id="quantidade" placeholder="Nova Quantidade" required>
            <input type="number" id="saida" placeholder="Nova Quantidade de Saída" required>
            <input type="date" id="data" required>
            <input type="text" id="setor" placeholder="Setor" required>
            <button type="submit">Atualizar</button>
        </form>
    `;
  
    document.getElementById('updateForm').addEventListener('submit', function (e) {
        e.preventDefault();
  
        // Obtém os valores dos campos
        let codigo = document.getElementById('codigo').value.trim();
        let quantidade = parseInt(document.getElementById('quantidade').value);
        let saida = parseInt(document.getElementById('saida').value);
        let data = document.getElementById('data').value.trim();
        let setor = document.getElementById('setor').value.trim();
  
        // Cria o objeto com dados atualizados
        const itemAtualizado = { 
            quantidade, 
            saida, 
            quantidadeAposSaida: quantidade - saida, // Recalcula o saldo
            data, 
            setor 
        };
  
        // Envia requisição PUT para a API
        fetch(`/api/items/${codigo}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itemAtualizado),
        })
        .then((res) => {
            if (!res.ok) throw new Error('Erro ao atualizar item');
            return res.json();
        })
        .then((data) => {
            console.log('Item atualizado:', data);
            viewInventory(); // Atualiza o inventário
            formContainer.innerHTML = ''; // Limpa o formulário
        })
        .catch((err) => console.error('Erro ao atualizar item:', err));
    });
}
  
// Função para exibir o formulário de remoção de itens
function showRemoveForm() {
    const formContainer = document.getElementById('form-container');
  
    formContainer.innerHTML = `
        <h2>Remover Item</h2>
        <form id="removeForm">
            <input type="text" id="codigoRemover" placeholder="Código do Produto" required>
            <button type="submit">Remover</button>
        </form>
    `;
  
    document.getElementById('removeForm').addEventListener('submit', function (e) {
        e.preventDefault();
  
        // Obtém o código do item a ser removido
        let codigo = document.getElementById('codigoRemover').value.trim();
  
        // Envia requisição DELETE para a API
        fetch(`/api/items/${codigo}`, {
            method: 'DELETE',
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.error) {
                alert(data.error); // Exibe erro se houver
            } else {
                viewInventory(); // Atualiza inventário em caso de sucesso
            }
            formContainer.innerHTML = ''; // Limpa o formulário
        })
        .catch((err) => console.error('Erro ao remover item:', err));
    });
}
  
// Função para exibir o inventário atual
function viewInventory() {
    const inventoryContainer = document.getElementById('inventory-container');
  
    // Busca os itens da API
    fetch('/api/items')
        .then((res) => res.json())
        .then((data) => {
            // Gera a tabela de inventário
            inventoryContainer.innerHTML = `
                <h2>Itens no Estoque</h2>
                <table>
                    <tr>
                        <th>Código</th>
                        <th>Nome</th>
                        <th>Quantidade</th>
                        <th>Saída</th>
                        <th>Quantidade Após Saída</th>
                        <th>Data</th>
                        <th>Setor</th>
                    </tr>
                    ${data
                        .map(
                            (item) => `
                        <tr>
                            <td>${item.codigo}</td>
                            <td>${item.nome}</td>
                            <td>${item.quantidade}</td>
                            <td>${item.saida}</td>
                            <td>${item.quantidadeAposSaida}</td>
                            <td>${item.data}</td>
                            <td>${item.setor}</td>
                        </tr>
                    `
                        )
                        .join('')} <!-- Converte array em string HTML -->
                </table>
            `;
        })
        .catch((err) => console.error('Erro ao buscar inventário:', err));
}
  
// Inicializa a exibição do inventário quando o documento é carregado
document.addEventListener('DOMContentLoaded', function () {
    viewInventory();
});
