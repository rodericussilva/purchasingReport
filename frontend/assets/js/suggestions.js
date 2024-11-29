let productsData = [];

document.addEventListener('DOMContentLoaded', function () {
    const suppliersDropdown = document.getElementById('suppliers-dropdown');
    const suppliersCheckboxesContainer = document.getElementById('suppliers-checkboxes');
    const selectAllCheckbox = document.getElementById('select-all');
    const replacementDaysInput = document.getElementById('replacementDays');
    const supplyDaysInput = document.getElementById('supplyDays');
    const calculateButton = document.getElementById('calculate-button');
    const generateReportButton = document.getElementById('generate-report-button');
    const fileFormatSelect = document.getElementById('choose-file');
    const dataTableContainer = document.getElementById('data-table-container');
    const reportSection = document.getElementById('report-generation-section');

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar fornecedores');
                }
                return response.json();
            })
            .then(suppliers => {
                if (suppliers.length === 0) {
                    suppliersCheckboxesContainer.innerHTML = '<div class="text-muted">Nenhum fornecedor disponível</div>';
                    return;
                }

                suppliers.forEach(supplier => {
                    const checkboxDiv = document.createElement('div');
                    checkboxDiv.classList.add('dropdown-item');
                    checkboxDiv.innerHTML = ` 
                        <input type="checkbox" id="supplier-${supplier.nome}" class="supplier-checkbox form-check-input me-2" value="${supplier.nome}">
                        <label for="supplier-${supplier.nome}" class="form-check-label">${supplier.nome}</label>
                    `;
                    suppliersCheckboxesContainer.appendChild(checkboxDiv);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar fornecedores:', error);
                suppliersCheckboxesContainer.innerHTML = '<div class="text-danger">Erro ao carregar fornecedores</div>';
            });
    }

    function updateDropdownButtonLabel() {
        const selectedCheckboxes = Array.from(document.querySelectorAll('.supplier-checkbox:checked'));
        if (selectedCheckboxes.length === 0) {
            suppliersDropdown.textContent = 'Selecionar Fornecedores';
        } else if (selectedCheckboxes.length === document.querySelectorAll('.supplier-checkbox').length) {
            suppliersDropdown.textContent = 'Todos os Fornecedores Selecionados';
        } else {
            suppliersDropdown.textContent = selectedCheckboxes.map(checkbox => checkbox.value).join(', ');
        }
    }

    selectAllCheckbox.addEventListener('change', function () {
        const isChecked = selectAllCheckbox.checked;
        document.querySelectorAll('.supplier-checkbox').forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        updateDropdownButtonLabel();
    });

    suppliersCheckboxesContainer.addEventListener('change', function () {
        const allCheckboxes = document.querySelectorAll('.supplier-checkbox');
        const selectedCheckboxes = Array.from(allCheckboxes).filter(checkbox => checkbox.checked);
        selectAllCheckbox.checked = selectedCheckboxes.length === allCheckboxes.length;
        updateDropdownButtonLabel();
    });

    function getProductsBySuppliers(suppliers, replacementDays, supplyDays) {
        const suppliersQuery = suppliers.map(supplier => `supplier_name[]=${encodeURIComponent(supplier)}`).join('&');
        const url = `${CONFIG.API_BASE_URL}/api/products?${suppliersQuery}&replacement_days=${replacementDays}&supply_days=${supplyDays}`;

        dataTableContainer.innerHTML = '';

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar produtos. Verifique os parâmetros e tente novamente.');
                }
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert('Nenhum produto encontrado para os fornecedores selecionados.');
                    return;
                }

                productsData = data;

                data.forEach(({ fornecedor, produtos }) => {
                    createTableForSupplier(fornecedor, produtos);
                });

                reportSection.style.display = 'block';
            })
            .catch(error => {
                console.error('Erro ao carregar produtos:', error);
            });
    }

    function createTableForSupplier(supplierName, products) {
        const supplierSection = document.createElement('div');
        supplierSection.classList.add('mb-4');
        
        const title = document.createElement('h5');
        title.textContent = `Fornecedor: ${supplierName}`;
        title.classList.add('mt-3', 'text-secundary');
        
        const tableWrapper = document.createElement('div');
        tableWrapper.classList.add('table-responsive');
        
        const table = document.createElement('table');
        table.classList.add('table', 'table-striped', 'table-bordered');
        
        const mesLabels = products[0].mes_labels;

        table.innerHTML = `
            <thead>
                <tr>
                    <th class="col-md-3 text-center">Descrição</th>
                    <th class="text-center">Cobertura</th>
                    <th class="text-center" colspan="4">Unidades Faturadas</th>
                    <th class="text-center">Méd. Mês</th>
                    <th class="text-center">Est. Disponível</th>
                    <th class="text-center">Est. Minimo</th>
                    <th class="text-center">Sugestão de Compra</th>
                    <th class="text-center">Valor de Compra</th>
                    <th class="text-center">Curva</th>
                </tr>
                <tr>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                    <th class="month text-center">${mesLabels.mes3}</th>
                    <th class="month text-center">${mesLabels.mes2}</th>
                    <th class="month text-center">${mesLabels.mes1}</th>
                    <th class="month text-center">${mesLabels.mes0}</th>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                    <th class="text-center"> - </th>
                </tr>
            </thead>
            <tbody>
                ${products
                    .map(product => `
                        <tr>
                            <td>${product.descricao}</td>
                            <td>${product.cobertura}</td>
                            <td>${product.unidades_faturadas_mes3}</td>
                            <td>${product.unidades_faturadas_mes2}</td>
                            <td>${product.unidades_faturadas_mes1}</td>
                            <td>${product.unidades_faturadas_mes0}</td>
                            <td>${product.media_faturada}</td>
                            <td>${product.estoque_disponivel}</td>
                            <td>${product.estoque_minimo}</td>
                            <td>${product.sugestao_compra}</td>
                            <td>${product.valor_venda}</td>
                            <td>${product.curva}</td>
                        </tr>`).join('')}
            </tbody>
        `;
        
        tableWrapper.appendChild(table);
        supplierSection.appendChild(title);
        supplierSection.appendChild(tableWrapper);
        dataTableContainer.appendChild(supplierSection);
    }

    calculateButton.addEventListener('click', function () {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const replacementDays = parseInt(replacementDaysInput.value, 10) || 0;
        const supplyDays = parseInt(supplyDaysInput.value, 10) || 0;

        if (selectedSuppliers.length === 0) {
            alert('Por favor, selecione pelo menos um fornecedor.');
            return;
        }

        if (replacementDays <= 0 || supplyDays <= 0) {
            alert('Por favor, insira valores válidos para dias de reposição e dias de suprimento.');
            return;
        }

        getProductsBySuppliers(selectedSuppliers, replacementDays, supplyDays);
    });

    generateReportButton.addEventListener('click', function () {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const replacementDays = parseInt(replacementDaysInput.value, 10) || 0;
        const supplyDays = parseInt(supplyDaysInput.value, 10) || 0;
        const fileFormat = fileFormatSelect.value;
    
        if (selectedSuppliers.length === 0 || replacementDays === 0 || supplyDays === 0 || !fileFormat) {
            alert('Preencha todos os campos antes de gerar o relatório.');
            return;
        }
    
        const productsData = [];
    
        dataTableContainer.querySelectorAll('.mb-4').forEach(supplierSection => {
            const supplierNameElement = supplierSection.querySelector('h5');
            
            if (!supplierNameElement) return;
    
            const supplierName = supplierNameElement.textContent.replace('Fornecedor: ', '');
            
            const products = [];
    
            supplierSection.querySelectorAll('tbody tr').forEach(row => {
                const productData = {
                    descricao: row.cells[0]?.textContent || '',
                    cobertura: row.cells[1]?.textContent || '',
                    unidades_faturadas_mes3: row.cells[2]?.textContent || '',
                    unidades_faturadas_mes2: row.cells[3]?.textContent || '',
                    unidades_faturadas_mes1: row.cells[4]?.textContent || '',
                    unidades_faturadas_mes0: row.cells[5]?.textContent || '',
                    media_faturada: row.cells[6]?.textContent || '',
                    estoque_disponivel: row.cells[7]?.textContent || '',
                    estoque_minimo: row.cells[8]?.textContent || '',
                    sugestao_compra: row.cells[9]?.textContent || '',
                    valor_venda: row.cells[10]?.textContent || '',
                    curva: row.cells[11]?.textContent || '',
                    mes_labels: {
                        mes0: row.cells[2]?.textContent || 'Mês 0',
                        mes1: row.cells[3]?.textContent || 'Mês 1',
                        mes2: row.cells[4]?.textContent || 'Mês 2',
                        mes3: row.cells[5]?.textContent || 'Mês 3',
                    }
                };
                products.push(productData);
            });
    
            productsData.push({ fornecedor: supplierName, produtos: products });
        });
    
        fetch(`${CONFIG.API_BASE_URL}/api/generate_report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                suppliers: selectedSuppliers,
                replacement_days: replacementDays,
                supply_days: supplyDays,
                table_data: productsData, 
                file_format: fileFormat
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.file_path) {
                window.open(data.file_path, '_blank');
            } else {
                alert('Erro ao gerar o relatório.');
            }
        })
        .catch(error => {
            console.error('Erro ao gerar relatório:', error);
            alert(`Erro ao gerar relatório, ${error}`);
        });
    });    

    getSuppliers();
});