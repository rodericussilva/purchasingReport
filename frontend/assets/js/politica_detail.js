document.addEventListener("DOMContentLoaded", function () {

    const calculateButton = document.getElementById("calculate-button");
    const sellersDropdown = document.getElementById("sellers-dropdown");
    const sellersCheckboxesContainer = document.getElementById("sellers-checkboxes");
    const selectAllCheckbox = document.getElementById("select-all");
    const monthSelect = document.getElementById("select-month");
    const yearSelect = document.getElementById("select-year");
    const dataTable = document.getElementById("data-table");
    const resultsSection = document.getElementById("results-section");

    let commissionsData = [];

    // Formatação de moeda
    const money = (v) =>
        Number(v || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

    function getSellers() {
        fetch(`${CONFIG.API_BASE_URL}/api/sellers`)
            .then(response => response.json())
            .then(sellers => {
                sellersCheckboxesContainer.innerHTML = "";
                sellers.forEach(seller => {
                    const checkboxDiv = document.createElement("div");
                    checkboxDiv.classList.add("dropdown-item");
                    checkboxDiv.innerHTML = `
                        <input type="checkbox" 
                               class="seller-checkbox form-check-input me-2" 
                               data-code="${seller.codigo}"
                               id="seller-${seller.codigo}" 
                               value="${seller.nome}">
                        <label for="seller-${seller.codigo}" class="form-check-label">
                            ${seller.nome}
                        </label>
                    `;
                    sellersCheckboxesContainer.appendChild(checkboxDiv);
                });
            });
    }

    function getPeriodsBySellers(sellerCodes) {
        const query = sellerCodes
            .map(code => `seller_code[]=${encodeURIComponent(code)}`)
            .join("&");

        fetch(`${CONFIG.API_BASE_URL}/api/sellers/periods?${query}`)
            .then(response => response.json())
            .then(periods => {
                monthSelect.innerHTML = '<option value="" disabled selected>Selecione um mês</option>';
                yearSelect.innerHTML = '<option value="" disabled selected>Selecione um ano</option>';

                if (!periods.length) return;

                const uniqueMonths = [...new Set(periods.map(p => p.mes))];
                const uniqueYears = [...new Set(periods.map(p => p.ano))];

                uniqueMonths.sort((a,b)=>a-b);
                uniqueYears.sort((a,b)=>b-a);

                uniqueMonths.forEach(month => {
                    const option = document.createElement("option");
                    option.value = month;
                    option.textContent = getMonthName(month);
                    monthSelect.appendChild(option);
                });

                uniqueYears.forEach(year => {
                    const option = document.createElement("option");
                    option.value = year;
                    option.textContent = year;
                    yearSelect.appendChild(option);
                });
            });
    }

    function getMonthName(monthNumber) {
        const months = [
            "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio",
            "Junho", "Julho", "Agosto", "Setembro", "Outubro",
            "Novembro", "Dezembro"
        ];
        return months[monthNumber];
    }

    function updateDropdownButtonLabel() {
        const selected = Array.from(document.querySelectorAll(".seller-checkbox:checked"));
        if (selected.length === 0) {
            sellersDropdown.textContent = "Selecionar Vendedor";
        } else if (selected.length === document.querySelectorAll(".seller-checkbox").length) {
            sellersDropdown.textContent = "Todos os Vendedores";
        } else {
            sellersDropdown.textContent = selected.map(cb => cb.value).join(", ");
        }
    }

    selectAllCheckbox.addEventListener("change", function () {
        const isChecked = selectAllCheckbox.checked;
        document.querySelectorAll(".seller-checkbox").forEach(cb => {
            cb.checked = isChecked;
        });

        const selectedCodes = Array
            .from(document.querySelectorAll(".seller-checkbox:checked"))
            .map(cb => cb.dataset.code);

        if (selectedCodes.length > 0) {
            getPeriodsBySellers(selectedCodes);
        }
        updateDropdownButtonLabel();
    });

    sellersCheckboxesContainer.addEventListener("change", function () {
        const selectedCheckboxes = Array.from(
            document.querySelectorAll(".seller-checkbox:checked")
        );
        const selectedSellerCodes = selectedCheckboxes.map(cb => cb.dataset.code);
        if (selectedSellerCodes.length > 0) {
            getPeriodsBySellers(selectedSellerCodes);
        }
        const all = document.querySelectorAll(".seller-checkbox");
        selectAllCheckbox.checked = selectedCheckboxes.length === all.length;
        updateDropdownButtonLabel();
    });

    function getCommissions(sellerCodes, month, year) {
        const sellersQuery = sellerCodes
            .map(code => `seller_code[]=${encodeURIComponent(code)}`)
            .join("&");

        const url = `${CONFIG.API_BASE_URL}/api/political-detail?${sellersQuery}&month=${month}&year=${year}`;

        dataTable.innerHTML = "";
        resultsSection.style.display = "none";
        calculateButton.disabled = true;
        calculateButton.textContent = "Calculando...";

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.length) {
                    alert("Nenhum dado encontrado.");
                    return;
                }
                commissionsData = data;
                renderTable(data);
                resultsSection.style.display = "block";
            })
            .finally(() => {
                calculateButton.disabled = false;
                calculateButton.textContent = "Calcular";
            });
    }

    function renderTable(data) {
        dataTable.innerHTML = "";

        data.forEach(seller => {
            const sellerSection = document.createElement("div");
            sellerSection.classList.add("mb-4");

            const title = document.createElement("h5");
            title.textContent = `${seller.vendedor}`;
            title.classList.add("mt-3", "text-light");

            const tableWrapper = document.createElement("div");
            tableWrapper.classList.add("table-responsive");

            const table = document.createElement("table");
            table.classList.add("table", "table-striped", "table-bordered", "text-center");

            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Política</th>
                        <th>Venda Líquida</th>
                        <th>Porcentagem</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    ${seller.dados.map(item => `
                        <tr>
                            <td>${item.politica}</td>
                            <td>${item.venda_liquida.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}</td>
                            <td>${item.percentual.toFixed(2)}%</td>
                            <td>${item.valor.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}</td>
                        </tr>
                    `).join("")}
                    <tr class="table-secondary fw-bold">
                        <td>-</td>
                        <td>${seller.total_venda_liquida.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}</td>
                        <td>-</td>
                        <td>${seller.total_valor.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}</td>
                    </tr>
                </tbody>
            `;

            tableWrapper.appendChild(table);
            sellerSection.appendChild(title);
            sellerSection.appendChild(tableWrapper);
            dataTable.appendChild(sellerSection);
        });
    }

    calculateButton.addEventListener("click", function () {
        const selectedSellerCodes = Array
            .from(document.querySelectorAll(".seller-checkbox:checked"))
            .map(cb => cb.dataset.code);

        const month = monthSelect.value;
        const year = yearSelect.value;

        if (!selectedSellerCodes.length || !month || !year) {
            alert("Selecione vendedores, mês e ano.");
            return;
        }

        getCommissions(selectedSellerCodes, month, year);
    });

    function exportToExcel() {
        if (!commissionsData || commissionsData.length === 0) {
            alert("Nenhum dado disponível para exportar. Calcule os dados primeiro.");
            return;
        }

        const wb = XLSX.utils.book_new();

        commissionsData.forEach(seller => {
            const rows = seller.dados.map(item => [
                item.politica,
                Number(item.venda_liquida || 0),
                Number(item.percentual || 0).toFixed(2) + "%",
                Number(item.valor || 0),
            ]);

            const totalRow = [
                "-",
                Number(seller.total_venda_liquida || 0),
                "-",
                Number(seller.total_valor || 0),
            ];

            const sheetData = [
                [`Vendedor: ${seller.vendedor}`],
                [],
                ["Política", "Venda Líquida", "Porcentagem", "Valor"],
                ...rows,
                totalRow,
            ];

            const ws = XLSX.utils.aoa_to_sheet(sheetData);

            ws["!cols"] = [
                { wch: 35 }, { wch: 20 }, { wch: 14 }, { wch: 20 },
            ];

            const sheetName = String(seller.vendedor || "Vendedor").substring(0, 31);
            XLSX.utils.book_append_sheet(wb, ws, sheetName);
        });

        const monthName = getMonthName(parseInt(monthSelect.value));
        const year = yearSelect.value;
        XLSX.writeFile(wb, `detalhe_politica_${monthName}_${year}.xlsx`);
    }

    document.getElementById("export-excel-button").addEventListener("click", exportToExcel);

    getSellers();
});
