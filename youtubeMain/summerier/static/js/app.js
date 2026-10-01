const form = document.getElementById("summary-form");
const loading = document.getElementById("loading");
const thumbnail = document.getElementById("thumbnail");
const summary = document.getElementById("summary");
const resultToolbar = document.getElementById("result-toolbar");
const sentimentBadge = document.getElementById("sentiment-badge");
const sentenceList = document.getElementById("sentence-list");
const viewSummaryBtn = document.getElementById("view-summary-btn");
const viewSentimentBtn = document.getElementById("view-sentiment-btn");
let curruntSummaryId=null

// Explicit color map — applied directly as inline styles so it can never
// silently fail due to CSS specificity, caching, or class-name mismatches.
const SENTIMENT_COLORS = {
    positive: { text: "#6fcf97", border: "#6fcf97", bg: "rgba(111, 207, 151, 0.08)" },
    negative: { text: "#e5654a", border: "#e5654a", bg: "rgba(229, 101, 74, 0.08)" },
    neutral:  { text: "#8b93a1", border: "#2e3542", bg: "transparent" }
};

// --- View toggle logic ---
function showSummaryView() {
    summary.style.display = "block";
    sentenceList.style.display = "none";
    viewSummaryBtn.classList.add("active");
    viewSentimentBtn.classList.remove("active");
}

function showSentimentView() {
    summary.style.display = "none";
    sentenceList.style.display = "flex";
    viewSentimentBtn.classList.add("active");
    viewSummaryBtn.classList.remove("active");
}

viewSummaryBtn.addEventListener("click", showSummaryView);
viewSentimentBtn.addEventListener("click", showSentimentView);

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    loading.style.display = "block";
    summary.innerHTML = "";
    thumbnail.style.display = "none";
    thumbnail.src = "";
    resultToolbar.style.display = "none";
    sentenceList.innerHTML = "";
    sentenceList.style.display = "none";
    summary.style.display = "block";

    // Extract values from form inputs
    const ytLink = document.getElementById("yt-link").value;
    const summaryType = document.getElementById("summary-type").value;
    const language = document.getElementById("language").value;

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch("/api/summary/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf
            },
            body: JSON.stringify({
                yt_link: ytLink,
                summary_type: summaryType,
                language: language
            })
        });

        const data = await response.json();
        curruntSummaryId=data.id
        loading.style.display = "none";

        if (!response.ok || data.error) {
            const errorMsg = data.error || "Failed to generate summary. Please try again.";
            summary.innerHTML = `<p class="error-msg" style="color: red;">${errorMsg}</p>`;
            return;
        }

        if (data.thumbnail_url) {
            thumbnail.src = data.thumbnail_url;
            thumbnail.style.display = "block";
        }

        // Parse markdown returned from Gemini
        summary.innerHTML = marked.parse(data.summary);

        // Build the sentence-by-sentence sentiment list (hidden until toggled)
        if (Array.isArray(data.sentence_result) && data.sentence_result.length > 0) {
            data.sentence_result.forEach((item) => {
                const key = String(item.sentiment || "neutral").toLowerCase();
                const colors = SENTIMENT_COLORS[key] || SENTIMENT_COLORS.neutral;

                const div = document.createElement("div");
                div.className = "sentence-item";
                div.textContent = item.sentence;
                div.style.color = colors.text;
                div.style.borderLeftColor = colors.border;
                div.style.backgroundColor = colors.bg;

                sentenceList.appendChild(div);
            });
        }

        // Overall sentiment pill + toolbar (only shown once we have a result)
        if (data.sentiment) {
            const key = String(data.sentiment).toLowerCase();
            const colors = SENTIMENT_COLORS[key] || SENTIMENT_COLORS.neutral;

            sentimentBadge.textContent = data.sentiment;
            sentimentBadge.style.color = colors.text;
            sentimentBadge.style.borderColor = colors.border;
            sentimentBadge.style.background = colors.bg;
        }

        resultToolbar.style.display = "flex";
        showSummaryView(); // always land on Summary first

    } catch (err) {
        loading.style.display = "none";
        summary.innerHTML = `<p class="error-msg" style="color: red;">An error occurred while connecting to the server.</p>`;
    }
});

function downloadPDF(){
    if(!curruntSummaryId){
        alert('first genrate the summry')
    }
    console.log("Summary ID:", curruntSummaryId);
    window.location.href=`/api/export/${curruntSummaryId}/`
}