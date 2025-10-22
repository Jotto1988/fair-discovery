(() => {
  const start = Date.now();
  let maxDepth = 0;
  let interactions = 0;

  window.addEventListener("scroll", () => {
    const depth = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    maxDepth = Math.max(maxDepth, depth);
  });

  ["click", "mousemove", "keydown"].forEach(evt => {
    window.addEventListener(evt, () => interactions++);
  });

  window.addEventListener("beforeunload", () => {
    const timeSpent = (Date.now() - start) / 1000;
    const score = Math.round((timeSpent * (maxDepth + 0.1) * (interactions + 1)) / 5);
    navigator.sendBeacon("fair-discovery/record.php", JSON.stringify({
      path: location.pathname,
      score
    }));
  });
})();