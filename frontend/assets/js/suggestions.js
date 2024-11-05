document.addEventListener('DOMContentLoaded', function() {
    const suppliersSelect = document.getElementById('suppliers');
    const dataTable = document.getElementById('data-table');
    const replacementDaysInput = document.getElementById('replacementDays');
    const supplyDaysInput = document.getElementById('supplyDays');
    const calculateButton = document.getElementById('calculate-button');
    const reportSection = document.getElementById('report-generation-section');
    const generateReportButton = document.getElementById('generate-report-button');
    const fileFormatSelect = document.getElementById('choose-file');

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

    function getProductsBySupplier(supplierName, replacementDays, supplyDays) {
        fetch(`${CONFIG.API_BASE_URL}/api/products?supplier_name=${encodeURIComponent(supplierName)}&replacement_days=${replacementDays}&supply_days=${supplyDays}`)
            .then(response => response.json())
            .then(products => {
                dataTable.innerHTML = '';

                if (products.length > 0) {
                    const { mes0, mes1, mes2, mes3 } = products[0].mes_labels;

                    // table header with the name of the months
                    document.querySelector('th.month.text-center:nth-child(3)').textContent = mes3;
                    document.querySelector('th.month.text-center:nth-child(4)').textContent = mes2;
                    document.querySelector('th.month.text-center:nth-child(5)').textContent = mes1;
                    document.querySelector('th.month.text-center:nth-child(6)').textContent = mes0;
                }

                products.forEach(product => {
                    const row = document.createElement('tr');

                    // column values
                    row.innerHTML = `
                        <td>${product.descricao}</td>
                        <td>${product.cobertura}</td>
                        <td>${product.unidades_faturadas_mes3}</td>
                        <td>${product.unidades_faturadas_mes2}</td>
                        <td>${product.unidades_faturadas_mes1}</td>
                        <td>${product.unidades_faturadas_mes0}</td>
                        <td>${product.media_faturada}</td>
                        <td>${product.estoque_disponivel}</td>
                        <td>${product.sugestao_compra}</td>
                        <td>${product.valor_compra}</td>
                        <td>${product.curva}</td>
                    `;

                    dataTable.appendChild(row);
                });

                dataTable.style.display = 'contents';
                reportSection.style.display = 'block';

            })
            .catch(error => console.error('Erro ao carregar produtos:', error));
    }

    suppliersSelect.addEventListener('change', function() {
        const selectedSupplier = suppliersSelect.value;
        if (selectedSupplier) {
            dataTable.innerHTML = '';
            dataTable.style.display = 'none';
            reportSection.style.display = 'none';
        }
    });

    calculateButton.addEventListener('click', function () {
        const selectedSupplier = suppliersSelect.value;
        const replacementDays = parseInt(replacementDaysInput.value) || 0;
        const supplyDays = parseInt(supplyDaysInput.value) || 0;

        if (selectedSupplier && replacementDays > 0 && supplyDays > 0) {
            getProductsBySupplier(selectedSupplier, replacementDays, supplyDays);
        } else {
            alert("Por favor, preencha todos os campos: fornecedor, dias de reposição e dias de suprimento.");
        }
    });

    // Lógica para geração de relatórios em diferentes formatos
    generateReportButton.addEventListener('click', function () {
        const format = fileFormatSelect.value;
        if (!format) {
            alert("Por favor, selecione um formato de relatório.");
            return;
        }

        fetch(`/generate-report?format=${format}`, {
            method: 'GET',
        })
        .then(response => {
            if (response.ok) return response.blob();
            throw new Error("Erro ao gerar relatório.");
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `relatorio.${format}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            console.error(error);
            alert("Erro ao gerar relatório. Por favor, tente novamente.");
        });
    });

    getSuppliers();
});