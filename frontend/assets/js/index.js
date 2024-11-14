document.addEventListener("DOMContentLoaded", function () {
    function animateProgress(start, end, duration, elementId) {
        const stepTime = Math.abs(Math.floor(duration / (end - start)));
        let current = start;
        const progressElement = document.getElementById(elementId);

        const interval = setInterval(function () {
            current += 1;
            progressElement.innerText = current;

            if (current >= end) {
                clearInterval(interval);
            }
        }, stepTime);
    }

    function loadTotalSuggestions() {
        const progressElement = document.getElementById("total-suggestions");
        const loadingSpinner = document.getElementById("loading-spinner");

        loadingSpinner.style.display = "inline-block";

        fetch(`${CONFIG.API_BASE_URL}/api/total-suggestions`)
            .then(response => response.json())
            .then(data => {
                if (data.total_suggestions !== undefined) {
                    const total = data.total_suggestions;
                    loadingSpinner.style.display = "none";
                    animateProgress(0, total, 2000, "total-suggestions");
                }
            })
            .catch(error => {
                console.error("Erro ao carregar total de sugestões de compra:", error);
                loadingSpinner.style.display = "none";
                progressElement.innerText = "Erro ao carregar dados";
            });
    }

    function loadRuptureRisk(days = 30) {
        const progressElement = document.getElementById("total-rupture-items");
        const loadingSpinnerRupture = document.getElementById("loading-spinner-rupture");

        loadingSpinnerRupture.style.display = "inline-block";

        fetch(`${CONFIG.API_BASE_URL}/api/rupture-risk-count?days_estimate=${days}`)
            .then(response => response.json())
            .then(data => {
                if (data.total_risk_items !== undefined) {
                    const total = data.total_risk_items;
                    loadingSpinnerRupture.style.display = "none";
                    animateProgress(0, total, 2000, "total-rupture-items");
                } else {
                    progressElement.innerText = "0";
                    console.error("Nenhum valor de risco de ruptura retornado.");
                }
            })
            .catch(error => {
                console.error("Erro ao carregar total de itens em risco de ruptura:", error);
                loadingSpinnerRupture.style.display = "none";
                progressElement.innerText = "Erro ao carregar dados";
            });
    }

    function updateRuptureDays(days) {
        const selectedDaysSpan = document.getElementById("selected-days");
        selectedDaysSpan.textContent = `| ${days} dias`;
        loadRuptureRisk(days);
    }

    // Configura o filtro de dias com valor padrão de 30 dias ao carregar a página
    const daysFilter = document.getElementById("days-filter");
    daysFilter.addEventListener("click", (event) => {
        const target = event.target;
        if (target.classList.contains("dropdown-item")) {
            event.preventDefault();
            const selectedDays = target.getAttribute("data-days");
            updateRuptureDays(selectedDays);
        }
    });

    // Carrega as contagens iniciais com o valor padrão de 30 dias
    loadTotalSuggestions();
    updateRuptureDays(30);
});