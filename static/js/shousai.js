document.addEventListener("DOMContentLoaded", initPage);

// --- デモデータ ---
const person = {
  id: 1,
  name: "山田 太郎",
  bday: "1947-08-12",
  sex: "男性",
  address: "茅ヶ崎市○○町"
};

const visits = [
  { date: "2025-10-20", staff: "包括支援センターA", type: "訪問", note: "服薬状況確認" },
  { date: "2025-10-15", staff: "保健師B", type: "電話", note: "家族から相談" },
];

function initPage() {
  renderPerson();
  renderVisits();
  renderDascItems();

  document.getElementById("addVisitBtn").addEventListener("click", addVisit);
  document.getElementById("downloadVisitCsv").addEventListener("click", exportVisitsCsv);
  document.getElementById("downloadDascCsv").addEventListener("click", exportDascCsv);
}

function renderPerson() {
  document.getElementById("pName").textContent = person.name;
  document.getElementById("pBday").textContent = person.bday;
  document.getElementById("pSex").textContent = person.sex;
  document.getElementById("pAddress").textContent = person.address;
}

function renderVisits() {
  const tbody = document.getElementById("visitBody");
  tbody.innerHTML = "";
  visits.forEach(v => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${v.date}</td><td>${v.staff}</td><td>${v.type}</td><td>${v.note}</td>`;
    tbody.appendChild(tr);
  });
}

function addVisit() {
  const date = document.getElementById("visitDate").value;
  const staff = document.getElementById("visitStaff").value;
  const type = document.getElementById("visitType").value;
  const note = document.getElementById("visitNote").value;
  if (!date || !note) {
    alert("日付と要点を入力してください");
    return;
  }
  visits.unshift({ date, staff, type, note });
  renderVisits();
  document.getElementById("visitForm").reset();
}

function renderDascItems() {
  const dascDiv = document.getElementById("dascList");
  for (let i = 1; i <= 21; i++) {
    const div = document.createElement("div");
    div.classList.add("input-group");
    div.innerHTML = `<label>Q${i}</label><select data-q="${i}">
      <option value="0">0</option>
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>`;
    dascDiv.appendChild(div);
  }
  dascDiv.addEventListener("change", calcDasc);
}

function calcDasc() {
  const vals = Array.from(document.querySelectorAll("#dascList select")).map(s => parseInt(s.value));
  const total = vals.reduce((a, b) => a + b, 0);
  document.getElementById("dascTotal").textContent = total;
  const judge = total >= 50 ? "重度" : total >= 30 ? "中等度" : "軽度";
  document.getElementById("dascJudge").textContent = judge;
}

function exportVisitsCsv() {
  const header = "日付,担当者,種類,要点\n";
  const rows = visits.map(v => `${v.date},${v.staff},${v.type},${v.note}`).join("\n");
  downloadFile(header + rows, "visit_records.csv");
}

function exportDascCsv() {
  const vals = Array.from(document.querySelectorAll("#dascList select")).map(s => s.value);
  const total = document.getElementById("dascTotal").textContent;
  const judge = document.getElementById("dascJudge").textContent;
  const csv = `合計,${total},判定,${judge}\n${vals.join(",")}`;
  downloadFile(csv, "dasc21.csv");
}

function downloadFile(text, filename) {
  const blob = new Blob([text], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}
