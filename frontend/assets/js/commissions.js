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

  // Mapa Televendas ↔ Vendedores
  const TELE_VENDAS_MAP = {
    149: { codigo: 80, nome: "NOME1" },
    144: { codigo: 80, nome: "NOME1" },
    137: { codigo: 178, nome: "NOME2" },
    84:  { codigo: 178, nome: "NOME2" },
    172: { codigo: 183, nome: "NOME3" },
    98:  { codigo: 183, nome: "NOME3" },
    129: { codigo: 195, nome: "NOME4" },
    131: { codigo: 195, nome: "NOME4" },
    156: { codigo: 169, nome: "NOME5" },
    119: { codigo: 169, nome: "NOME5" },
    117: { codigo: 180, nome: "NOME6" },
    130: { codigo: 180, nome: "NOME6" },
    155: { codigo: 150, nome: "NOME7" },
    148: { codigo: 150, nome: "NOME7" },
    145: { codigo: 179, nome: "NOME8" },
    143: { codigo: 179, nome: "NOME8" },
  };

  function getSellers() {
    fetch(`${CONFIG.API_BASE_URL}/api/sellers`)
      .then((response) => response.json())
      .then((sellers) => {
        sellersCheckboxesContainer.innerHTML = "";
        sellers.forEach((seller) => {
          const checkboxDiv = document.createElement("div");
          checkboxDiv.classList.add("dropdown-item");
          checkboxDiv.innerHTML = `
            <input type="checkbox" class="seller-checkbox form-check-input me-2" data-code="${seller.codigo}" id="seller-${seller.codigo}" value="${seller.nome}">
            <label for="seller-${seller.codigo}" class="form-check-label">
              ${seller.nome}
            </label>
          `;
          sellersCheckboxesContainer.appendChild(checkboxDiv);
        });
      });
  }

  function getPeriodsBySellers(sellerCodes) {
    const query = sellerCodes.map((code) => `seller_code[]=${encodeURIComponent(code)}`).join("&");
    fetch(`${CONFIG.API_BASE_URL}/api/sellers/periods?${query}`)
      .then((response) => response.json())
      .then((periods) => {
        monthSelect.innerHTML = '<option value="" disabled selected>Selecione um mês</option>';
        yearSelect.innerHTML = '<option value="" disabled selected>Selecione um ano</option>';

        if (!periods.length) return;

        const uniqueMonths = [...new Set(periods.map((p) => p.mes))];
        const uniqueYears = [...new Set(periods.map((p) => p.ano))];

        uniqueMonths.sort((a, b) => a - b);
        uniqueYears.sort((a, b) => b - a);

        uniqueMonths.forEach((month) => {
          const option = document.createElement("option");
          option.value = month;
          option.textContent = getMonthName(month);
          monthSelect.appendChild(option);
        });
        uniqueYears.forEach((year) => {
          const option = document.createElement("option");
          option.value = year;
          option.textContent = year;
          yearSelect.appendChild(option);
        });
      });
  }

  function getMonthName(monthNumber) {
    const months = [
      "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
      "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
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
      sellersDropdown.textContent = selected.map((cb) => cb.value).join(", ");
    }
  }

  selectAllCheckbox.addEventListener("change", function () {
    const isChecked = selectAllCheckbox.checked;
    document.querySelectorAll(".seller-checkbox").forEach((cb) => {
      cb.checked = isChecked;
    });

    const selectedCodes = Array.from(document.querySelectorAll(".seller-checkbox:checked")).map(
      (cb) => cb.dataset.code
    );

    if (selectedCodes.length > 0) {
      getPeriodsBySellers(selectedCodes);
    }
    updateDropdownButtonLabel();
  });

  sellersCheckboxesContainer.addEventListener("change", function () {
    const selectedCheckboxes = Array.from(document.querySelectorAll(".seller-checkbox:checked"));
    const selectedSellerCodes = selectedCheckboxes.map((cb) => cb.dataset.code);
    if (selectedSellerCodes.length > 0) {
      getPeriodsBySellers(selectedSellerCodes);
    }
    const all = document.querySelectorAll(".seller-checkbox");
    selectAllCheckbox.checked = selectedCheckboxes.length === all.length;
    updateDropdownButtonLabel();
  });

  function getCommissions(sellerCodes, month, year) {
    const sellersQuery = sellerCodes
      .map((code) => `seller_code[]=${encodeURIComponent(code)}`)
      .join("&");

    const commissionsUrl = `${CONFIG.API_BASE_URL}/api/commissions?${sellersQuery}&month=${month}&year=${year}`;
    const politicalUrl = `${CONFIG.API_BASE_URL}/api/political-detail?${sellersQuery}&month=${month}&year=${year}`;

    dataTable.innerHTML = "";
    resultsSection.style.display = "none";
    calculateButton.disabled = true;
    calculateButton.textContent = "Calculando...";

    Promise.all([fetch(commissionsUrl).then((r) => r.json()), fetch(politicalUrl).then((r) => r.json())])
      .then(([commissions, political]) => {
        if (!Array.isArray(commissions) || commissions.length === 0) {
          alert("Nenhum dado encontrado em /api/commissions.");
          return;
        }

        const politicalByCode = new Map();
        political.forEach((s) => {
          const key = s.codigo_vendedor != null ? String(s.codigo_vendedor) : null;
          if (key) {
            politicalByCode.set(key, s);
          }
        });

        const politicalByName = new Map();
        if (politicalByCode.size === 0) {
          political.forEach((s) => {
            if (s.vendedor) politicalByName.set(s.vendedor.trim().toLowerCase(), s);
          });
        }

        const merged = commissions.map((c) => {
          const codeKey = c.codigo_vendedor != null ? String(c.codigo_vendedor) : null;
          const pol =
            codeKey && politicalByCode.size > 0
              ? politicalByCode.get(codeKey)
              : politicalByName.get((c.vendedor || "").trim().toLowerCase());

          const totalPolitica = Number(pol?.total_valor || 0);
          const totalPremiacao = Number(c.total_premiacao || 0);
          return {
            ...c,
            total_comissao: totalPremiacao + totalPolitica,
          };
        });

        commissionsData = merged;
        renderTable(merged);
        resultsSection.style.display = "block";
      })
      .catch((err) => {
        console.error("Erro ao calcular comissões:", err);
        alert("Ocorreu um erro ao calcular as comissões. Tente novamente.");
      })
      .finally(() => {
        calculateButton.disabled = false;
        calculateButton.textContent = "Calcular";
      });
  }

  function renderTable(data) {
    dataTable.innerHTML = "";

    data.forEach((seller) => {
      const sellerSection = document.createElement("div");
      sellerSection.classList.add("mb-4");

      const title = document.createElement("h5");
      title.textContent = `${seller.vendedor}`;
      title.classList.add("mt-3", "text-light");

      const link = document.createElement("a");
      link.href = "political-detail.html";
      link.textContent = " Detalhe por Política";
      link.classList.add("ms-2", "small");

      const totalSeller = document.createElement("span");
      totalSeller.textContent = `| Total realizado: ${money(seller.total_realizado_geral)}`;
      totalSeller.classList.add("ms-2", "small");

      const objective = document.createElement("span");
      objective.textContent = `| Objetivo: ${money(seller.objetivo_geral)}`;
      objective.classList.add("ms-2", "small");

      const coverage = document.createElement("span");
      coverage.textContent = `| Cobertura: ${Number(seller.cobertura || 0).toFixed(2)}%`;
      coverage.classList.add("ms-2", "small");

      const totalCommission = document.createElement("span");
      totalCommission.textContent = `| Comissão Total: ${money(seller.total_comissao)}`;
      totalCommission.classList.add("ms-2", "small");

      const tableWrapper = document.createElement("div");
      tableWrapper.classList.add("table-responsive");

      const table = document.createElement("table");
      table.classList.add("table", "table-striped", "table-bordered", "text-center");

      const vendedorCodigo = seller.codigo_vendedor != null ? seller.codigo_vendedor : seller.codigo;
      const tv =
        TELE_VENDAS_MAP[String(vendedorCodigo)] ||
        TELE_VENDAS_MAP[vendedorCodigo] ||
        null;

      const tvPercent = tv ? 0.30 : 0;
      let totalPremiacaoTv = 0;

      const dados = Array.isArray(seller.dados) ? seller.dados : [];

      const linhasBody = dados
        .map((item) => {
          const valorPremiacao = Number(item.valor_premiacao || 0);
          const valorPremiacaoTv = tvPercent * valorPremiacao;
          totalPremiacaoTv += valorPremiacaoTv;

          return `
            <tr>
              <td>${item.fabricante ?? "-"}</td>
              <td>${money(item.valor_realizado)}</td>
              <td>${money(item.valor_cota)}</td>
              <td>${Number(item.percentual_cobertura || 0).toFixed(2)}%</td>
              <td>${money(item.valor_devolucao)}</td>
              <td>${money(valorPremiacao)}</td>
              <td>${money(valorPremiacaoTv)}</td>
            </tr>
          `;
        })
        .join("");

      table.innerHTML = `
        <thead>
          <tr>
            <th>Fabricante</th>
            <th>Venda Realizada</th>
            <th>Objetivo</th>
            <th>% Cobertura</th>
            <th>Devolução</th>
            <th>Premiação RCA</th>
            <th>Premiação TV</th>
          </tr>
        </thead>
        <tbody>
          ${linhasBody}
          <tr class="table-secondary fw-bold">
            <td>TOTAL</td>
            <td>${money(seller.total_realizado)}</td>
            <td>-</td>
            <td>-</td>
            <td>${money(seller.total_devolucao)}</td>
            <td>${money(seller.total_premiacao)}</td>
            <td>${money(totalPremiacaoTv)}</td>
          </tr>
        </tbody>
      `;

      const summaryBar = document.createElement("div");
      summaryBar.className =
        "seller-summary-bar d-flex flex-wrap align-items-center gap-3 px-2 py-2 mt-2";

      const tvNomeCodigo = tv ? `${tv.codigo} - ${tv.nome}` : "—";
      const tvPremiacaoValor = totalPremiacaoTv;

      summaryBar.innerHTML = `
        <span class="text-light">Televendas: <strong class="text-light">${tvNomeCodigo}</strong></span>
        <span class="text-light">| Premiação Televendas (30%): <strong class="text-light">${money(tvPremiacaoValor)}</strong></span>
        <span class="text-light">| <strong class="text-success"></strong></span>
      `;

      tableWrapper.appendChild(table);
      sellerSection.appendChild(title);
      sellerSection.appendChild(tableWrapper);

      title.appendChild(link);
      title.appendChild(totalSeller);
      title.appendChild(objective);
      title.appendChild(coverage);
      title.appendChild(totalCommission);

      sellerSection.appendChild(summaryBar);
      dataTable.appendChild(sellerSection);
    });
  }

  calculateButton.addEventListener("click", function () {
    const selectedSellerCodes = Array.from(document.querySelectorAll(".seller-checkbox:checked")).map(
      (cb) => cb.dataset.code
    );
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
      alert("Nenhum dado disponível para exportar. Calcule as comissões primeiro.");
      return;
    }

    const wb = XLSX.utils.book_new();

    commissionsData.forEach((seller) => {
      const vendedorCodigo = seller.codigo_vendedor != null ? seller.codigo_vendedor : seller.codigo;
      const tv = TELE_VENDAS_MAP[String(vendedorCodigo)] || TELE_VENDAS_MAP[vendedorCodigo] || null;
      const tvPercent = tv ? 0.30 : 0;

      const dados = Array.isArray(seller.dados) ? seller.dados : [];
      let totalPremiacaoTv = 0;

      const rows = dados.map((item) => {
        const valorPremiacao = Number(item.valor_premiacao || 0);
        const valorPremiacaoTv = tvPercent * valorPremiacao;
        totalPremiacaoTv += valorPremiacaoTv;
        return [
          item.fabricante ?? "-",
          Number(item.valor_realizado || 0),
          Number(item.valor_cota || 0),
          Number(item.percentual_cobertura || 0).toFixed(2) + "%",
          Number(item.valor_devolucao || 0),
          valorPremiacao,
          valorPremiacaoTv,
        ];
      });

      const totalRow = [
        "TOTAL",
        Number(seller.total_realizado || 0),
        "-",
        "-",
        Number(seller.total_devolucao || 0),
        Number(seller.total_premiacao || 0),
        totalPremiacaoTv,
      ];

      const tvNomeCodigo = tv ? `${tv.codigo} - ${tv.nome}` : "—";

      const sheetData = [
        [`Vendedor: ${seller.vendedor}`],
        [
          `Total Realizado: ${money(seller.total_realizado_geral)}`,
          `Objetivo: ${money(seller.objetivo_geral)}`,
          `Cobertura: ${Number(seller.cobertura || 0).toFixed(2)}%`,
          `Comissão Total: ${money(seller.total_comissao)}`,
        ],
        [],
        ["Fabricante", "Venda Realizada", "Objetivo", "% Cobertura", "Devolução", "Premiação RCA", "Premiação TV"],
        ...rows,
        totalRow,
        [],
        [`Televendas: ${tvNomeCodigo}`, `Premiação Televendas (30%): ${money(totalPremiacaoTv)}`],
      ];

      const ws = XLSX.utils.aoa_to_sheet(sheetData);

      ws["!cols"] = [
        { wch: 30 }, { wch: 18 }, { wch: 18 }, { wch: 14 },
        { wch: 18 }, { wch: 18 }, { wch: 18 },
      ];

      // Nome da aba (máx 31 chars — limite do Excel)
      const sheetName = String(seller.vendedor || "Vendedor").substring(0, 31);
      XLSX.utils.book_append_sheet(wb, ws, sheetName);
    });

    const monthName = getMonthName(parseInt(monthSelect.value));
    const year = yearSelect.value;
    XLSX.writeFile(wb, `comissoes_${monthName}_${year}.xlsx`);
  }

  document.getElementById("export-excel-button").addEventListener("click", exportToExcel);

  getSellers();
});
