document.addEventListener('DOMContentLoaded', function () {
    const suppliersSelect = document.getElementById('suppliers');
    const calculateButton = document.getElementById('calculate-button');
    const dataTableBody = document.getElementById('data-table');
    const generateReportButton = document.getElementById('generate-report-button');
    const chooseFileSelect = document.getElementById('choose-file');

    function formatDateToBrazilian(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}-${month}-${year}`;
    }

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

    function getItemsBelow1Year(supplierName) {
        const url = `${CONFIG.API_BASE_URL}/api/items-below-1-year?supplier_name=${encodeURIComponent(supplierName)}`;
        
        fetch(url)
            .then(async response => {
                if (!response.ok) {
                    const errorData = await response.json();
                    const errorMessage = errorData.error || 'Erro desconhecido ao carregar itens.';
                    throw new Error(errorMessage);
                }
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert(`${supplierName} não possui itens abaixo de 1 ano para vencimento.`);
                } else {
                    populateTable(data);
                    document.getElementById('report-generation-section').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Erro ao carregar itens abaixo de 1 ano:', error.message);
                alert(`Erro ao carregar itens: ${error.message}`);
            });
    }

    function populateTable(items) {
        dataTableBody.innerHTML = '';

        items.forEach(item => {
            const formattedDate = formatDateToBrazilian(item.data_vencimento);
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="text-center">${item.descricao}</td>
                <td class="text-center">${item.quantidade_estoque}</td>
                <td class="text-center">${formattedDate}</td>
                <td class="text-center">${item.curva}</td>
            `;
            dataTableBody.appendChild(row);
        });
    }

    function generateReport() {
        const supplierName = suppliersSelect.value;
        const fileFormat = chooseFileSelect.value;

        if (!supplierName || !fileFormat) {
            alert("Preencha todos os campos antes de gerar o relatório.");
            return;
        }

        const tableData = Array.from(dataTableBody.querySelectorAll('tr')).map(row => {
            return Array.from(row.querySelectorAll('td')).map(cell => cell.textContent.trim());
        });

        const payload = {
            supplier_name: supplierName,
            table_data: tableData,
            file_format: fileFormat
        };

        fetch(`${CONFIG.API_BASE_URL}/api/generate_expiration_report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
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
    }

    calculateButton.addEventListener('click', function () {
        const supplierName = suppliersSelect.value;

        if (!supplierName) {
            alert('Por favor, selecione um fornecedor.');
            return;
        }

        getItemsBelow1Year(supplierName);
    });

    generateReportButton.addEventListener('click', generateReport);

    getSuppliers();
});
