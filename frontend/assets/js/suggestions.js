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
    
                    // Coluna Descrição
                    const descricaoCell = document.createElement('td');
                    descricaoCell.textContent = product.descricao;
                    row.appendChild(descricaoCell);
    
                    // Coluna Cobertura (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Cobertura
    
                    // Coluna Unidades Faturadas
                    const unidadesFaturadasCell = document.createElement('td');
                    unidadesFaturadasCell.textContent = product.unidades_faturadas_mes1 || 0; // Mes1
                    row.appendChild(unidadesFaturadasCell);
    
                    // Colunas para Unidades Faturadas Mes2 e Mes3
                    const mes2Cell = document.createElement('td');
                    mes2Cell.textContent = product.unidades_faturadas_mes2 || 0; // Mes2
                    row.appendChild(mes2Cell);
    
                    const mes3Cell = document.createElement('td');
                    mes3Cell.textContent = product.unidades_faturadas_mes3 || 0; // Mes3
                    row.appendChild(mes3Cell);
    
                    // Coluna Méd. Mês (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Méd. Mês
    
                    // Coluna Est. Min. (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Est. Min.
    
                    // Coluna Est. Supr. (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Est. Supr.
    
                    // Coluna Est. Disponível (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Est. Disponível
    
                    // Coluna Sugestão de Compra (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Sugestão de Compra
    
                    // Coluna Valor de Compra (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Valor de Compra
    
                    // Coluna Curva
                    const curvaCell = document.createElement('td');
                    curvaCell.textContent = product.curva || 'N/A'; // Curva
                    row.appendChild(curvaCell);
    
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
