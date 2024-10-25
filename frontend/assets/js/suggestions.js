document.addEventListener('DOMContentLoaded', function() {
    const suppliersSelect = document.getElementById('suppliers');
    const dataTable = document.getElementById('data-table');

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar fornecedores');
                }
                return response.json();
            })
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

    function getProductsBySupplier(supplierName) {
        fetch(`${CONFIG.API_BASE_URL}/api/products?supplier_name=${encodeURIComponent(supplierName)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar produtos');
                }
                return response.json();
            })
            .then(products => {
                dataTable.innerHTML = ''; // Limpa a tabela antes de adicionar os novos dados

                products.forEach(product => {
                    const row = document.createElement('tr');

                    const descricaoCell = document.createElement('td');
                    descricaoCell.textContent = product.descricao;
                    row.appendChild(descricaoCell);

                    // Adicione aqui as células vazias ou com valores padrão para os demais dados da tabela
                    row.appendChild(document.createElement('td')); // Cobertura
                    row.appendChild(document.createElement('td')); // Mês 1
                    row.appendChild(document.createElement('td')); // Mês 2
                    row.appendChild(document.createElement('td')); // Mês 3
                    row.appendChild(document.createElement('td')); // Méd. Mês
                    row.appendChild(document.createElement('td')); // Est. Min.
                    row.appendChild(document.createElement('td')); // Est. Supr.
                    row.appendChild(document.createElement('td')); // Est. Disponível
                    row.appendChild(document.createElement('td')); // Sugestão de Compra
                    row.appendChild(document.createElement('td')); // Valor de Compra
                    row.appendChild(document.createElement('td'));

                    dataTable.appendChild(row);
                });
            })
            .catch(error => console.error('Erro ao carregar produtos:', error));
    }

    suppliersSelect.addEventListener('change', function() {
        const selectedSupplier = suppliersSelect.value;
        if (selectedSupplier) {
            getProductsBySupplier(selectedSupplier);
        }
    });

    getSuppliers();
});
