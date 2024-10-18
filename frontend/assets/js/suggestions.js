document.addEventListener('DOMContentLoaded', function() {
    const suppliersSelect = document.getElementById('suppliers')

    function getSuppliers() {
        fetch(`${CONFIG.API_BASE_URL}/api/suppliers`).then(response => {
            if (!response.ok) {
                throw new  Error('Erro ao buscar fornecedores');
            }
            return response.json();
        }).then(suppliers => {
            //suppliersSelect.innerHTML = '<option value=""disabled selected>Selecione um fornecedor</option>';

            suppliers.forEach(supply => {
                const option = document.createElement('option');
                option.value = supply.nome;
                option.textContent = supply.nome
                suppliersSelect.appendChild(option)
            });
        }).catch(error => console.error('Erro ao carregar fornecedores:', error));
    }

    getSuppliers();
});