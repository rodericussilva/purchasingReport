document.addEventListener('DOMContentLoaded', function () {
    const suppliersDropdown = document.getElementById('suppliers-dropdown');
    const suppliersCheckboxesContainer = document.getElementById('suppliers-checkboxes');
    const selectAllCheckbox = document.getElementById('select-all');
    const daysSelect = document.getElementById('count-days');
    const calculateButton = document.getElementById('calculate-button');
    const dataTableContainer = document.getElementById('data-table');
    const reportSection = document.getElementById('report-generation-section');
    const generateReportButton = document.getElementById('generate-report-button');
    const fileFormatSelect = document.getElementById('choose-file');
    let itemsData = [];

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => {
                if (!response.ok) throw new Error("Erro ao buscar fornecedores.");
                return response.json();
            })
            .then(suppliers => {
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
            .catch(error => console.error("Erro ao carregar fornecedores:", error));
    }

    function updateDropdownLabel() {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        suppliersDropdown.textContent = selectedSuppliers.length > 0 ? selectedSuppliers.join(", ") : "Selecionar Fornecedores";
    }

    selectAllCheckbox.addEventListener('change', function () {
        const isChecked = selectAllCheckbox.checked;
        document.querySelectorAll('.supplier-checkbox').forEach(checkbox => (checkbox.checked = isChecked));
        updateDropdownLabel();
    });

    suppliersCheckboxesContainer.addEventListener('change', updateDropdownLabel);

    function getStagnantItems(suppliers, days) {
        const suppliersQuery = suppliers.map(supplier => `supplier_name[]=${encodeURIComponent(supplier)}`).join('&');
        const url = `${CONFIG.API_BASE_URL}/api/stagnant-items?${suppliersQuery}&days=${days}`;

        dataTableContainer.innerHTML = '';
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error("Erro ao buscar itens parados.");
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert("Nenhum item parado encontrado.");
                    return;
                }

                itemsData = data;
                data.forEach(supplierData => {
                    createTableForSupplier(supplierData.fornecedor, supplierData.produtos);
                });

                reportSection.style.display = 'block';
            })
            .catch(error => console.error("Erro ao carregar itens parados:", error));
    }

    function createTableForSupplier(supplierName, products) {
        const supplierSection = document.createElement("div");
        supplierSection.classList.add("mb-4");

        const title = document.createElement("h5");
        title.textContent = `Fornecedor: ${supplierName}`;
        title.classList.add("mt-3", "text-secundary");

        const tableWrapper = document.createElement("div");
        tableWrapper.classList.add("table-responsive");

        const table = document.createElement("table");
        table.classList.add("table", "table-striped", "table-bordered");

        table.innerHTML = `
            <thead>
                <tr>
                    <th class="text-center">Descrição</th>
                    <th class="text-center">Quantidade em Estoque</th>
                    <th class="text-center">Data da Última Venda</th>
                    <th class="text-center">Curva</th>
                </tr>
            </thead>
            <tbody>
                ${products.map(product => `
                    <tr>
                        <td class="text-center">${product.descricao}</td>
                        <td class="text-center">${product.quantidade_estoque}</td>
                        <td class="text-center">${product.ultima_venda}</td>
                        <td class="text-center">${product.curva}</td>
                    </tr>
                `).join("")}
            </tbody>
        `;

        tableWrapper.appendChild(table);
        supplierSection.appendChild(title);
        supplierSection.appendChild(tableWrapper);
        dataTableContainer.appendChild(supplierSection);
    }

    function generateReport() {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const days = daysSelect.value;
        const fileFormat = fileFormatSelect.value;

        if (!selectedSuppliers.length || !days || !fileFormat) {
            alert("Preencha todos os campos para gerar o relatório.");
            return;
        }

        const payload = { suppliers: selectedSuppliers, days, table_data: itemsData, file_format: fileFormat };

        fetch(`${CONFIG.API_BASE_URL}/api/generate-stagnant-report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                if (data.file_path) {
                    window.open(data.file_path, '_blank');
                } else {
                    alert("Erro ao gerar o relatório.");
                }
            })
            .catch(error => console.error("Erro ao gerar relatório:", error));
    }

    calculateButton.addEventListener('click', function () {
        const selectedSuppliers = Array.from(document.querySelectorAll('.supplier-checkbox:checked')).map(checkbox => checkbox.value);
        const days = daysSelect.value;

        if (!selectedSuppliers.length || !days) {
            alert("Selecione pelo menos um fornecedor e insira um número de dias.");
            return;
        }

        getStagnantItems(selectedSuppliers, days);
    });

    generateReportButton.addEventListener('click', generateReport);

    getSuppliers();
});