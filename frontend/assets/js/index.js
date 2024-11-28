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

    function loadItemsStopped(days = 120) {
        const progressElement = document.getElementById("total-stopped-120-days");
        const loadingSpinnerStopped120 = document.getElementById("loading-spinner-120");
        const stoppedCardTitle = document.querySelector(".superior-card .card-title");

        loadingSpinnerStopped120.style.display = "inline-block";

        fetch(`${CONFIG.API_BASE_URL}/api/items-stopped?days=${days}`)
            .then(response => response.json())
            .then(data => {
                if (data.total_stopped_items !== undefined) {
                    const total = data.total_stopped_items;
                    loadingSpinnerStopped120.style.display = "none";
                    animateProgress(0, total, 2000, "total-stopped-120-days");

                    stoppedCardTitle.innerHTML = `Itens parados a mais de ${days} dias <span></span>`;
                } else {
                    progressElement.innerText = "0";
                }
            })
            .catch(error => {
                console.error(`Erro ao carregar itens parados a mais de ${days} dias:`, error);
                loadingSpinnerStopped120.style.display = "none";
                progressElement.innerText = "Erro ao carregar dados";
            });
    }

    function loadItemsWithin1Year() {
        const progressElement = document.getElementById("total-maturity-items");
        const loadingSpinnerMaturity = document.getElementById("loading-spinner-maturity");

        loadingSpinnerMaturity.style.display = "inline-block";

        fetch(`${CONFIG.API_BASE_URL}/api/maturity-items-count`)
            .then(response => response.json())
            .then(data => {
                if (data.total_within_1_year !== undefined) {
                    const total = data.total_within_1_year;
                    loadingSpinnerMaturity.style.display = "none";
                    animateProgress(0, total, 2000, "total-maturity-items");
                } else {
                    progressElement.innerText = "0";
                    console.error("Nenhum valor de itens abaixo de 1 ano retornado.");
                }
            })
            .catch(error => {
                console.error("Erro ao carregar total de itens abaixo de 1 ano:", error);
                loadingSpinnerMaturity.style.display = "none";
                progressElement.innerText = "Erro ao carregar dados";
            });
    }

    function updateStoppedItemsFilter(days) {
        loadItemsStopped(days);
    }

    function updateRuptureDays(days) {
        const selectedDaysSpan = document.getElementById("selected-days");
        selectedDaysSpan.textContent = `| ${days} dias`;
        loadRuptureRisk(days);
    }

    const ruptureDaysFilter = document.getElementById("rupture-days-filter");
    ruptureDaysFilter.addEventListener("click", (event) => {
        const target = event.target;
        if (target.classList.contains("dropdown-item")) {
            event.preventDefault();
            const selectedDays = parseInt(target.getAttribute("data-days"), 10);
            updateRuptureDays(selectedDays);
        }
    });

    const stoppedDaysFilter = document.getElementById("stopped-days-filter");
    stoppedDaysFilter.addEventListener("click", (event) => {
        const target = event.target;
        if (target.classList.contains("dropdown-item")) {
            event.preventDefault();
            const selectedDays = parseInt(target.getAttribute("data-days"), 10);
            updateStoppedItemsFilter(selectedDays);
        }
    });

    loadTotalSuggestions();
    updateRuptureDays(30); // Default value for rupture risk
    loadItemsStopped(120); // Default value for stopped items
    loadItemsWithin1Year();
});