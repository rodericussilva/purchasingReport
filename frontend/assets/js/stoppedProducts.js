document.addEventListener('DOMContentLoaded', function () {
    const suppliersSelect = document.getElementById('suppliers');
    const calculateButton = document.getElementById('calculate-button');
    const dataTableBody = document.getElementById('data-table');

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => response.json())
            .then(suppliers => {
                suppliersSelect.innerHTML = '<option value="" disabled selected>Selecione um fornecedor</option>';
                suppliers.forEach(supplier => {
                    const option = document.createElement('option');
                    option.value = supplier.nome;
                    option.textContent = supplier.nome;
                    suppliersSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Erro ao carregar fornecedores:', error));
    }

    function getStagnantItems(supplierName) {
        const url = `${CONFIG.API_BASE_URL}/api/stagnant-items?supplier_name=${encodeURIComponent(supplierName)}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor.');
                }
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert(`${supplierName} não possui itens parados há mais de 120 dias.`);
                } else {
                    populateTable(data);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar itens parados:', error);
                alert('Erro ao carregar dados. Verifique o console para mais detalhes.');
            });
    }

    function populateTable(items) {
        dataTableBody.innerHTML = '';

        items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="text-center">${item.descricao}</td>
                <td class="text-center">${item.quantidade_estoque}</td>
                <td class="text-center">${item.ultima_venda}</td>
                <td class="text-center">${item.curva}</td>
            `;
            dataTableBody.appendChild(row);
        });
    }

    calculateButton.addEventListener('click', function () {
        const supplierName = suppliersSelect.value;

        if (!supplierName) {
            alert('Por favor, selecione um fornecedor.');
            return;
        }

        getStagnantItems(supplierName);
    });

    getSuppliers();
});
