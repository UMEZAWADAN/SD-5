// ===== タブ切り替え =====
document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const tab = btn.dataset.tab;
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        document.getElementById(tab).classList.add("active");
    });
});

// ===== まとめて保存 =====
document.getElementById("saveAllBtn").addEventListener("click", async () => {

    const payload = {
        kihon: document.getElementById("kihon_form").value,
        kiroku: document.getElementById("kiroku_form").value,
        shintai: document.getElementById("shintai_form").value,
        dasc21: document.getElementById("dasc21_form").value,
        dbd13: document.getElementById("dbd13_form").value
    };

    const res = await fetch("/api/save_all_assessments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const result = await res.json();
    alert(result.status === "ok" ? "保存しました ✅" : "保存に失敗しました ❌");
});
