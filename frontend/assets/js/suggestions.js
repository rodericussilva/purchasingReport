document.addEventListener('DOMContentLoaded', function() {
    const suppliersSelect = document.getElementById('suppliers');
    const dataTable = document.getElementById('data-table');

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => {
                if (!response.ok) throw new Error('Erro ao buscar fornecedores');
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
                if (!response.ok) throw new Error('Erro ao buscar produtos');
                return response.json();
            })
            .then(products => {
                dataTable.innerHTML = ''; // Limpa a tabela antes de adicionar os novos dados
                
                if (products.length > 0) {
                    const { mes0, mes1, mes2, mes3 } = products[0].mes_labels;

                    // Atualiza os cabeçalhos da tabela com os rótulos dos meses
                    document.querySelector('th.month.text-center:nth-child(3)').textContent = mes0;
                    document.querySelector('th.month.text-center:nth-child(4)').textContent = mes1;
                    document.querySelector('th.month.text-center:nth-child(5)').textContent = mes2;
                    document.querySelector('th.month.text-center:nth-child(6)').textContent = mes3;
                }

                products.forEach(product => {
                    const row = document.createElement('tr');

                    // Adiciona as colunas com os valores específicos
                    row.innerHTML = `
                        <td>${product.descricao}</td>
                        <td>${product.cobertura}</td>
                        <td>${product.unidades_faturadas_mes3}</td>
                        <td>${product.unidades_faturadas_mes2}</td>
                        <td>${product.unidades_faturadas_mes1}</td>
                        <td>${product.unidades_faturadas_mes0}</td>
                        <td>${product.media_faturada}</td>
                        <td>${product.estoque_minimo}</td>
                        <td>${product.estoque_suprimento}</td>
                        <td>${product.estoque_disponivel}</td>
                        <td>${product.sugestao_compra}</td>
                        <td>${product.valor_compra}</td>
                        <td>${product.curva}</td>
                    `;

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