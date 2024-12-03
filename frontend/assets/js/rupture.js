document.addEventListener("DOMContentLoaded", function () {
    const calculateRiskButton = document.getElementById("calculate-risk-button");
    const generateReportButton = document.getElementById("generate-report-button");
    const chooseFileSelect = document.getElementById("choose-file");
    const suppliersRiskDropdown = document.getElementById("suppliers-risk-dropdown");
    const suppliersRiskCheckboxesContainer = document.getElementById("suppliers-risk-checkboxes");
    const selectAllRiskCheckbox = document.getElementById("select-all-risk");
    const riskDaysInput = document.getElementById("riskDays");
    const dataTableContainer = document.getElementById("risk-data-table-container");
    const reportSection = document.getElementById("report-generation-section");

    let suppliersData = [];

    // Função para obter os fornecedores
    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro ao buscar fornecedores.");
                }
                return response.json();
            })
            .then(suppliers => {
                if (suppliers.length === 0) {
                    suppliersRiskCheckboxesContainer.innerHTML = '<div class="text-muted">Nenhum fornecedor disponível</div>';
                    return;
                }

                suppliers.forEach(supplier => {
                    const checkboxDiv = document.createElement("div");
                    checkboxDiv.classList.add("dropdown-item");
                    checkboxDiv.innerHTML = `
                        <input type="checkbox" id="supplier-risk-${supplier.nome}" class="supplier-risk-checkbox form-check-input me-2" value="${supplier.nome}">
                        <label for="supplier-risk-${supplier.nome}" class="form-check-label">${supplier.nome}</label>
                    `;
                    suppliersRiskCheckboxesContainer.appendChild(checkboxDiv);
                });
            })
            .catch(error => {
                console.error("Erro ao carregar fornecedores:", error);
                suppliersRiskCheckboxesContainer.innerHTML = '<div class="text-danger">Erro ao carregar fornecedores</div>';
            });
    }

    // Atualiza o botão dropdown com os fornecedores selecionados
    function updateDropdownButtonLabel() {
        const selectedCheckboxes = Array.from(document.querySelectorAll(".supplier-risk-checkbox:checked"));
        if (selectedCheckboxes.length === 0) {
            suppliersRiskDropdown.textContent = "Selecionar Fornecedores";
        } else if (selectedCheckboxes.length === document.querySelectorAll(".supplier-risk-checkbox").length) {
            suppliersRiskDropdown.textContent = "Todos os Fornecedores Selecionados";
        } else {
            suppliersRiskDropdown.textContent = selectedCheckboxes.map(checkbox => checkbox.value).join(", ");
        }
    }

    // Selecionar todos os fornecedores
    selectAllRiskCheckbox.addEventListener("change", function () {
        const isChecked = selectAllRiskCheckbox.checked;
        document.querySelectorAll(".supplier-risk-checkbox").forEach(checkbox => {
            checkbox.checked = isChecked;
        });
        updateDropdownButtonLabel();
    });

    suppliersRiskCheckboxesContainer.addEventListener("change", function () {
        const allCheckboxes = document.querySelectorAll(".supplier-risk-checkbox");
        const selectedCheckboxes = Array.from(allCheckboxes).filter(checkbox => checkbox.checked);
        selectAllRiskCheckbox.checked = selectedCheckboxes.length === allCheckboxes.length;
        updateDropdownButtonLabel();
    });

    function getRiskBySuppliers(suppliers, daysEstimate) {
        const suppliersQuery = suppliers.map(supplier => `supplier_name[]=${encodeURIComponent(supplier)}`).join("&");
        const url = `${CONFIG.API_BASE_URL}/api/rupture-risk?${suppliersQuery}&days_estimate=${daysEstimate}`;

        dataTableContainer.innerHTML = "";

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro ao buscar produtos com risco de ruptura.");
                }
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert("Nenhum produto encontrado com risco de ruptura para os fornecedores selecionados.");
                    return;
                }

                suppliersData = data;

                data.forEach(({ fornecedor, produtos }) => {
                    createTableForSupplier(fornecedor, produtos);
                });

                reportSection.style.display = "block";
            })
            .catch(error => {
                console.error("Erro ao buscar dados:", error);
            });
    }

    function createTableForSupplier(supplierName, products) {
        const supplierSection = document.createElement("div");
        supplierSection.classList.add("mb-4");

        const title = document.createElement("h5");
        title.textContent = `Fornecedor: ${supplierName}`;
        title.classList.add("mt-3", "text-danger");

        const tableWrapper = document.createElement("div");
        tableWrapper.classList.add("table-responsive");

        const table = document.createElement("table");
        table.classList.add("table", "table-striped", "table-bordered");

        table.innerHTML = `
            <thead>
                <tr>
                    <th class="text-center">Descrição</th>
                    <th class="text-center">Est. Disponível</th>
                    <th class="text-center">Estoque Min.</th>
                    <th class="text-center">Em trânsito</th>
                    <th class="text-center">Média diária</th>
                    <th class="text-center">Curva</th>
                </tr>
            </thead>
            <tbody>
                ${products.map(product => `
                    <tr>
                        <td class="text-center">${product.descricao}</td>
                        <td class="text-center">${product.estoque_disponivel}</td>
                        <td class="text-center">${product.estoque_minimo}</td>
                        <td class="text-center">${product.estoque_transito}</td>
                        <td class="text-center">${product.media_diaria_venda}</td>
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

    // Função para gerar o relatório
    function generateReport() {
        const selectedSuppliers = Array.from(document.querySelectorAll(".supplier-risk-checkbox:checked")).map(checkbox => checkbox.value);
        const daysEstimate = parseInt(riskDaysInput.value, 10) || 0;
        const fileFormat = chooseFileSelect.value;

        if (selectedSuppliers.length === 0 || daysEstimate === 0 || !fileFormat) {
            alert("Preencha todos os campos antes de gerar o relatório.");
            return;
        }

        const productsData = suppliersData.map(({ fornecedor, produtos }) => ({ fornecedor, produtos }));

        const payload = {
            suppliers: selectedSuppliers,
            days_estimate: daysEstimate,
            table_data: productsData,
            file_format: fileFormat
        };

        fetch(`${CONFIG.API_BASE_URL}/api/generate_rupture_report`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                if (data.file_path) {
                    window.open(data.file_path, "_blank");
                } else {
                    alert("Erro ao gerar o relatório.");
                }
            })
            .catch(error => {
                console.error("Erro ao gerar relatório:", error);
                alert("Erro ao gerar relatório.");
            });
    }

    calculateRiskButton.addEventListener("click", function () {
        const selectedSuppliers = Array.from(document.querySelectorAll(".supplier-risk-checkbox:checked")).map(checkbox => checkbox.value);
        const daysEstimate = riskDaysInput.value;

        if (selectedSuppliers.length === 0 || !daysEstimate) {
            alert("Por favor, selecione pelo menos um fornecedor e insira os dias estimados.");
            return;
        }

        getRiskBySuppliers(selectedSuppliers, daysEstimate);
    });

    generateReportButton.addEventListener("click", generateReport);

    getSuppliers();
});