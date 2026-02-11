const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const sendWhatsappBtn = document.getElementById("sendWhatsappBtn");
const loader = document.getElementById("loader");
const resultSection = document.querySelector(".result-section");

analyzeBtn.addEventListener("click", async () => {

    const text = document.getElementById("textInput").value;
    const url = document.getElementById("urlInput").value;

    if (!text && !url) {
        alert("Please enter text or URL to analyze.");
        return;
    }

    loader.classList.remove("hidden");

    try {
        const response = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text, url })
        });

        const data = await response.json();

        displayResult(data);

    } catch (error) {
        alert("Error connecting to server.");
    }

    loader.classList.add("hidden");
});

clearBtn.addEventListener("click", () => {
    document.getElementById("textInput").value = "";
    document.getElementById("urlInput").value = "";
});

sendWhatsappBtn.addEventListener("click", async () => {

    const phone = document.getElementById("phoneNumber").value;

    if (!phone) {
        alert("Enter phone number.");
        return;
    }

    await fetch("http://localhost:5000/send-whatsapp-alert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone })
    });

    alert("WhatsApp alert sent!");
});

function displayResult(data) {

    resultSection.classList.remove("hidden");

    const score = data.risk_score || 0;

    document.getElementById("scoreValue").innerText = score + "%";
    document.getElementById("analysisExplanation").innerText = data.explanation;
    document.getElementById("riskLabel").innerText = score > 70 ? "High Risk ⚠️" :
                                                     score > 40 ? "Medium Risk" :
                                                     "Low Risk ✔️";
}
