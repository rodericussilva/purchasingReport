document.addEventListener("DOMContentLoaded", function() {
    function animateProgress(start, end, duration) {
      const stepTime = Math.abs(Math.floor(duration / (end - start)));
      let current = start;
      const progressElement = document.getElementById("total-suggestions");
  
      const interval = setInterval(function() {
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
  
      // Chama a API
      fetch(`${CONFIG.API_BASE_URL}/api/total_suggestions`)
        .then(response => response.json())
        .then(data => {
          if (data.total_suggestions) {
            const total = data.total_suggestions;
            loadingSpinner.style.display = "none";
            animateProgress(0, total, 2000);
          }
        })
        .catch(error => {
          console.error("Erro ao carregar total de sugestões de compra:", error);
          loadingSpinner.style.display = "none";
          progressElement.innerText = "Erro ao carregar dados";
        });
    }
  
    loadTotalSuggestions();
});  