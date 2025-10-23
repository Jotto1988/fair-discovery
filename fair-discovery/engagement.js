(() => {
  const start = Date.now();
  let maxDepth = 0;
  let interactions = 0;

  window.addEventListener("scroll", () => {
    const depth = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    maxDepth = Math.max(maxDepth, depth);
    console.log("[FairDiscovery] Scroll depth:", maxDepth);
  });

  ["click", "mousemove", "keydown"].forEach(evt => {
    window.addEventListener(evt, () => {
      interactions++;
      console.log("[FairDiscovery] Interaction:", evt, interactions);
    });
  });

  window.addEventListener("beforeunload", (e) => {
    const timeSpent = (Date.now() - start) / 1000;
    const score = Math.round((timeSpent * (maxDepth + 0.1) * (interactions + 1)) / 5);
    console.log("[FairDiscovery] Sending data:", { path: location.pathname, score });

    const data = JSON.stringify({ path: location.pathname, score });
    const url = "/fair-discovery/record.php";

    // Try sendBeacon first
    const beaconSuccess = navigator.sendBeacon(url, data);
    console.log("[FairDiscovery] sendBeacon success:", beaconSuccess);

    // Fallback to fetch with keepalive if sendBeacon fails
    if (!beaconSuccess) {
      fetch(url, {
        method: "POST",
        body: data,
        keepalive: true // Ensures request completes after unload
      }).then(response => {
        console.log("[FairDiscovery] Fetch fallback response:", response.status);
      }).catch(error => {
        console.log("[FairDiscovery] Fetch fallback error:", error);
      });
    }
  });

  console.log("[FairDiscovery] FairDiscovery tracker initialized ✅");
})();