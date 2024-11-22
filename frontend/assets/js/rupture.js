document.addEventListener("DOMContentLoaded", function () {
    const calculateButton = document.getElementById("calculate-button");
    const generateReportButton = document.getElementById("generate-report-button");
    const chooseFileSelect = document.getElementById("choose-file");
    const suppliersSelect = document.getElementById("suppliers");
    const replacementDaysInput = document.getElementById("days-estemate");
    const dataTableBody = document.getElementById("data-table");
    const reportSection = document.getElementById("report-generation-section");

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

    function populateTable(products) {
        dataTableBody.innerHTML = "";

        products.forEach(product => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td class="text-center">${product.descricao}</td>
                <td class="text-center">${product.estoque_disponivel}</td>
                <td class="text-center">${product.estoque_minimo}</td>
                <td class="text-center">${product.estoque_transito}</td>
                <td class="text-center">${product.media_diaria_venda}</td>
                <td class="text-center">${product.curva}</td>
            `;
            dataTableBody.appendChild(row);
        });

        // Exibe a seção de geração de relatório
        reportSection.style.display = "block";
    }

    function getRuptureRisk(supplierName, daysEstimate) {
        const url = `${CONFIG.API_BASE_URL}/api/rupture-risk?supplier_name=${supplierName}&days_estimate=${daysEstimate}`;

        fetch(url.trim())
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro na resposta do servidor.");
                }
                return response.json();
            })
            .then(data => {
                if (Array.isArray(data) && data.length === 0) {
                    alert(`${supplierName} não possui produtos em movimentação no estoque.`);
                } else if (data && Array.isArray(data)) {
                    populateTable(data);
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Erro ao buscar dados: ${error.message}`);
            });
    }

    function generateReport() {
        const supplierName = suppliersSelect.value; 
        const daysEstimate = replacementDaysInput.value;
        const fileFormat = chooseFileSelect.value;
    
        if (!supplierName || !daysEstimate || !fileFormat) {
            alert("Preencha todos os campos antes de gerar o relatório.");
            return;
        }
    
        const tableData = Array.from(dataTableBody.querySelectorAll("tr")).map(row => {
            return Array.from(row.querySelectorAll("td")).map(cell => cell.textContent.trim());
        });
    
        const payload = {
            supplier: supplierName,
            days_estimate: parseInt(daysEstimate, 10),
            table_data: tableData,
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

    calculateButton.addEventListener("click", function () {
        const supplierName = suppliersSelect ? suppliersSelect.value : null;
        const daysEstimate = replacementDaysInput ? replacementDaysInput.value : null;

        if (!supplierName || !daysEstimate) {
            alert("Por favor, selecione um fornecedor e insira os dias estimados.");
            return;
        }

        getRuptureRisk(supplierName, daysEstimate);
    });

    generateReportButton.addEventListener("click", generateReport);

    getSuppliers();
});