document.addEventListener("DOMContentLoaded", function () {
    const calculateButton = document.getElementById("calculate-button");
    const suppliersSelect = document.getElementById("suppliers");
    const replacementDaysInput = document.getElementById("days-estemate");
    const dataTableBody = document.getElementById("data-table");

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
                <td class="text-center">${product.estoque_fisico}</td>
                <td class="text-center">${product.estoque_disponivel}</td>
                <td class="text-center">${product.estoque_minimo}</td>
                <td class="text-center">${product.estoque_transito}</td>
                <td class="text-center">${product.media_diaria_venda}</td>
                <td class="text-center">${product.curva}</td>
            `;
            dataTableBody.appendChild(row);
        });
    }

    function getRuptureRisk(supplierName, daysEstimate) {
        const url = `${CONFIG.API_BASE_URL}/api/rupture-risk?supplier_name=${supplierName}&days_estimate=${daysEstimate}`;
    
        fetch(url.trim())
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        return response.json().then(data => {
                            if (data.message && data.message === "Nenhum produto encontrado para o fornecedor especificado!") {
                                alert(`${supplierName} não possui produtos em movimentação no estoque.`);
                            } else {
                                alert(`Erro inesperado: ${data.message || "Não foi possível processar a requisição."}`);
                            }
                        });
                    } else {
                        throw new Error(`Erro na resposta do servidor: ${response.statusText}`);
                    }
                }
                return response.json();
            })
            .then(data => {
                if (Array.isArray(data) && data.length === 0) {
                    alert(`${supplierName} não possui produtos em movimentação no estoque.`);
                } else if (data && Array.isArray(data)) {
                    populateTable(data);
                } else {
                    alert("Erro inesperado ao processar os dados do fornecedor.");
                }
            })
            .catch(error => {
                console.error('Erro na requisição:', error);
                alert(`Entrar em contato com o suporte. Erro ao buscar dados: ${error.message}`);
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

    getSuppliers();
});