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
                
                // Atualiza cabeçalhos da tabela
                const monthAbbreviations = ['MAR', 'ABR', 'MAI']; // Placeholder para meses
                // Aqui você deve fazer uma chamada para a API que retorna as abreviações
                fetch(`${CONFIG.API_BASE_URL}/api/month-abbreviations`)
                    .then(response => response.json())
                    .then(abbr => {
                        monthAbbreviations[0] = abbr.mes1; // Mes 1
                        monthAbbreviations[1] = abbr.mes2; // Mes 2
                        monthAbbreviations[2] = abbr.mes3; // Mes 3
                        
                        // Atualiza os cabeçalhos da tabela
                        document.querySelector('th.month.text-center:nth-child(3)').textContent = monthAbbreviations[0];
                        document.querySelector('th.month.text-center:nth-child(4)').textContent = monthAbbreviations[1];
                        document.querySelector('th.month.text-center:nth-child(5)').textContent = monthAbbreviations[2];
                    });

                products.forEach(product => {
                    const row = document.createElement('tr');

                    // Coluna Descrição
                    const descricaoCell = document.createElement('td');
                    descricaoCell.textContent = product.descricao;
                    row.appendChild(descricaoCell);

                    // Coluna Cobertura (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Cobertura

                    const mes3Cell = document.createElement('td');
                    mes3Cell.textContent = product.unidades_faturadas_mes3 || 0; // Mês 3
                    row.appendChild(mes3Cell);

                    const mes2Cell = document.createElement('td');
                    mes2Cell.textContent = product.unidades_faturadas_mes2 || 0; // Mês 2
                    row.appendChild(mes2Cell);

                    // Colunas de Unidades Faturadas
                    const unidadesFaturadasCell = document.createElement('td');
                    unidadesFaturadasCell.textContent = product.unidades_faturadas_mes1 || 0; // Mês 1
                    row.appendChild(unidadesFaturadasCell);

                    // Colunas restantes (sem dados por enquanto)
                    row.appendChild(document.createElement('td')); // Méd. Mês
                    row.appendChild(document.createElement('td')); // Est. Min.
                    row.appendChild(document.createElement('td')); // Est. Supr.
                    row.appendChild(document.createElement('td')); // Est. Disponível
                    row.appendChild(document.createElement('td')); // Sugestão de Compra
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
