function showAddForm() {
    const formContainer = document.getElementById('form-container');
  
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
  
    document.getElementById('addForm').addEventListener('submit', function (e) {
        e.preventDefault();
  
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
  
        const novoItem = { codigo, nome, quantidade, saida, quantidadeAposSaida: quantidade - saida, data, setor };
  
        fetch('/api/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(novoItem),
        })
            .then((res) => res.json())
            .then((data) => {
                console.log('Item adicionado:', data);
                viewInventory();
                formContainer.innerHTML = '';
            })
            .catch((err) => console.error('Erro ao adicionar item:', err));
    });
  }
  
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
  
        let codigo = document.getElementById('codigo').value.trim();
        let quantidade = parseInt(document.getElementById('quantidade').value);
        let saida = parseInt(document.getElementById('saida').value);
        let data = document.getElementById('data').value.trim();
        let setor = document.getElementById('setor').value.trim();
  
        const itemAtualizado = { quantidade, saida, quantidadeAposSaida: quantidade - saida, data, setor };
  
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
                viewInventory();
                formContainer.innerHTML = '';
            })
            .catch((err) => console.error('Erro ao atualizar item:', err));
    });
  }
  
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
  
        let codigo = document.getElementById('codigoRemover').value.trim();
  
        fetch(`/api/items/${codigo}`, {
            method: 'DELETE',
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.error) {
                    alert(data.error);
                } else {
                    viewInventory();
                }
                formContainer.innerHTML = '';
            })
            .catch((err) => console.error('Erro ao remover item:', err));
    });
  }
  
  function viewInventory() {
    const inventoryContainer = document.getElementById('inventory-container');
  
    fetch('/api/items')
        .then((res) => res.json())
        .then((data) => {
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
                        .join('')}
                </table>
            `;
        })
        .catch((err) => console.error('Erro ao buscar inventário:', err));
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    viewInventory();
  });
