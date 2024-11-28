document.addEventListener('DOMContentLoaded', function () {
    const suppliersSelect = document.getElementById('suppliers');
    const daysSelect = document.getElementById('count-days');
    const calculateButton = document.getElementById('calculate-button');
    const dataTableBody = document.getElementById('data-table');
    const reportSection = document.getElementById('report-generation-section');
    const generateReportButton = document.getElementById('generate-report-button');
    const chooseFileSelect = document.getElementById('choose-file');

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

    function getStagnantItems(supplierName, days) {
        const url = `${CONFIG.API_BASE_URL}/api/stagnant-items?supplier_name=${encodeURIComponent(supplierName)}&days=${days}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor.');
                }
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    alert(`${supplierName} não possui itens parados há mais de ${days} dias.`);
                } else {
                    populateTable(data);
                    reportSection.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Erro ao carregar itens parados:', error);
                alert('Erro ao carregar dados. Verifique o console para mais detalhes.');
            });
    }

    function populateTable(items) {
        dataTableBody.innerHTML = '';

        items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="text-center">${item.descricao}</td>
                <td class="text-center">${item.quantidade_estoque}</td>
                <td class="text-center">${item.ultima_venda}</td>
                <td class="text-center">${item.curva}</td>
            `;
            dataTableBody.appendChild(row);
        });
    }

    function generateReport() {
        const supplierName = suppliersSelect.value;
        const fileFormat = chooseFileSelect.value;

        if (!supplierName || !fileFormat) {
            alert('Preencha todos os campos antes de gerar o relatório.');
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

        fetch(`${CONFIG.API_BASE_URL}/api/generate-stagnant-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
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
        const days = daysSelect.value;

        if (!supplierName || !days) {
            alert('Por favor, selecione um fornecedor e uma quantidade de dias.');
            return;
        }

        getStagnantItems(supplierName, days);
    });

    generateReportButton.addEventListener('click', generateReport);

    getSuppliers();
});