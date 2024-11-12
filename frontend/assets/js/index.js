document.addEventListener('DOMContentLoaded', function() {
    fetch(`${CONFIG.API_BASE_URL}/api/total_suggestions`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar os dados');
            }
            return response.json();
        })
        .then(data => {
            const totalSuggestions = data.total_suggestions || 0;
            console.log("Total de sugestões:", totalSuggestions);
            document.querySelector('.card-body h6').textContent = totalSuggestions;
        })
        .catch(error => {
            console.error('Erro ao carregar total de sugestões de compra:', error);
            document.querySelector('.card-body h6').textContent = "Erro ao carregar dados.";
        });
});
