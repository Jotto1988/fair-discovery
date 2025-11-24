(() => {
  async function loadInsights() {
    try {
      const res = await fetch("discovery.json?" + Date.now());
      const data = await res.json();

      if (!data.pages || !Array.isArray(data.pages)) {
        document.getElementById("insights").innerHTML = "<p>No valid data yet.</p>";
        return;
      }

      // Sort pages by engagement score
      const sorted = [...data.pages].sort((a, b) => b.score - a.score);

      // Basic stats
      const totalScore = sorted.reduce((a, b) => a + b.score, 0);
      const top3 = sorted.slice(0, 3);
      const avg = totalScore / sorted.length;

      let insightsHTML = `
        <h2>AI Engagement Insights 🤖</h2>
        <p><strong>Total pages tracked:</strong> ${sorted.length}</p>
        <p><strong>Average engagement score:</strong> ${avg.toFixed(2)}</p>
        <hr>
        <h3>🔥 Top 3 Most Engaging Pages</h3>
        <ul>
          ${top3
            .map(
              (p) => `<li><strong>${p.url}</strong> — score: ${p.score}</li>`
            )
            .join("")}
        </ul>
      `;

      // Pattern detection (simple offline AI logic)
      const patternMessages = [];
      if (avg > 100) patternMessages.push("Your site shows strong overall engagement — great user retention.");
      if (avg < 20) patternMessages.push("Engagement seems low. Consider adding visuals, FAQs, or calls-to-action.");
      if (sorted.length > 5 && sorted[0].score > avg * 3)
        patternMessages.push(`Page "${sorted[0].url}" dominates engagement — maybe feature it more prominently.`);
      if (sorted.length > 3 && sorted[sorted.length - 1].score < avg / 3)
        patternMessages.push(`Some pages perform poorly — revisit layout or content relevance.`);

      insightsHTML += `<hr><h3>🧭 Recommendations</h3><ul>${patternMessages
        .map((m) => `<li>${m}</li>`)
        .join("")}</ul>`;

      document.getElementById("insights").innerHTML = insightsHTML;
    } catch (err) {
      document.getElementById("insights").innerHTML = `<p>Error loading insights: ${err.message}</p>`;
    }
  }

  document.addEventListener("DOMContentLoaded", loadInsights);
})();
