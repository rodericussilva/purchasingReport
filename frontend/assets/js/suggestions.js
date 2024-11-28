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
        dataTableContainer.innerHTML = '';
        suppliers.forEach(supplierName => {
            fetch(`${CONFIG.API_BASE_URL}/api/products?supplier_name=${encodeURIComponent(supplierName)}&replacement_days=${replacementDays}&supply_days=${supplyDays}`)
                .then(response => response.json())
                .then(products => {
                    if (products.length > 0) {
                        createTableForSupplier(supplierName, products);
                    } else {
                        console.warn(`Nenhum produto encontrado para o fornecedor: ${supplierName}`);
                    }
                })
                .catch(error => console.error(`Erro ao carregar produtos para o fornecedor ${supplierName}:`, error));
        });
    }

    function createTableForSupplier(supplierName, products) {
        const supplierSection = document.createElement('div');
        supplierSection.classList.add('mb-4');

        const title = document.createElement('h5');
        title.textContent = `Fornecedor: ${supplierName}`;
        title.classList.add('mt-3', 'text-primary');

        const table = document.createElement('table');
        table.classList.add('table', 'table-striped', 'table-bordered');
        table.innerHTML = `
            <thead>
                <tr>
                    <th class="text-center">Descrição</th>
                    <th class="text-center">Cobertura</th>
                    <th class="text-center">Mês 0</th>
                    <th class="text-center">Mês 1</th>
                    <th class="text-center">Mês 2</th>
                    <th class="text-center">Mês 3</th>
                    <th class="text-center">Méd. Mês</th>
                    <th class="text-center">Est. Disponível</th>
                    <th class="text-center">Est. Mínimo</th>
                    <th class="text-center">Sugestão de Compra</th>
                    <th class="text-center">Valor de Compra</th>
                    <th class="text-center">Curva</th>
                </tr>
            </thead>
            <tbody>
                ${products
                    .map(product => `
                        <tr>
                            <td>${product.descricao}</td>
                            <td>${product.cobertura}</td>
                            <td>${product.unidades_faturadas_mes0}</td>
                            <td>${product.unidades_faturadas_mes1}</td>
                            <td>${product.unidades_faturadas_mes2}</td>
                            <td>${product.unidades_faturadas_mes3}</td>
                            <td>${product.media_faturada}</td>
                            <td>${product.estoque_disponivel}</td>
                            <td>${product.estoque_minimo}</td>
                            <td>${product.sugestao_compra}</td>
                            <td>${product.valor_venda}</td>
                            <td>${product.curva}</td>
                        </tr>`).join('')}
            </tbody>
        `;

        supplierSection.appendChild(title);
        supplierSection.appendChild(table);
        dataTableContainer.appendChild(supplierSection);
    }

    calculateButton.addEventListener('click', function () {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const replacementDays = parseInt(replacementDaysInput.value) || 0;
        const supplyDays = parseInt(supplyDaysInput.value) || 0;

        if (selectedSuppliers.length > 0 && replacementDays > 0 && supplyDays > 0) {
            getProductsBySuppliers(selectedSuppliers, replacementDays, supplyDays);
        } else {
            alert('Por favor, preencha todos os campos: fornecedores, dias de reposição e dias de suprimento.');
        }
    });

    generateReportButton.addEventListener('click', function () {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const replacementDays = parseInt(replacementDaysInput.value) || 0;
        const supplyDays = parseInt(supplyDaysInput.value) || 0;
        const fileFormat = fileFormatSelect.value;

        if (selectedSuppliers.length === 0 || replacementDays === 0 || supplyDays === 0 || !fileFormat) {
            alert('Preencha todos os campos antes de gerar o relatório.');
            return;
        }

        fetch(`${CONFIG.API_BASE_URL}/api/generate_report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                suppliers: selectedSuppliers,
                replacement_days: replacementDays,
                supply_days: supplyDays,
                file_format: fileFormat,
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
                alert('Erro ao gerar relatório. Verifique o console para mais detalhes.');
            });
    });

    getSuppliers();
});