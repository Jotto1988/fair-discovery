(() => {
  const start = Date.now();
  let maxDepth = 0;
  let interactions = 0;
  let pixelFired = false;

  // ----------------------------------------------------
  // 🟢 CONFIGURATION: ENTER YOUR PIXEL ID BELOW
  // ----------------------------------------------------
  const FACEBOOK_PIXEL_ID = "YOUR_PIXEL_ID_HERE"; 
  // ----------------------------------------------------

  // Function to ignite Facebook Pixel only when called
  function triggerSmartPixel() {
    if (pixelFired) return; // Only fire once per session
    pixelFired = true;

    console.log("[FairDiscovery] Human detected. Firing Facebook Pixel... 🎯");

    // Standard Facebook Code (Wrapped)
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');

    fbq('init', FACEBOOK_PIXEL_ID);
    fbq('track', 'PageView'); 
  }

  // 1. Scroll Detection
  window.addEventListener("scroll", () => {
    const depth = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    maxDepth = Math.max(maxDepth, depth);
    
    // If they scroll more than 1%, they are likely human. Fire Pixel.
    if (maxDepth > 0.01) triggerSmartPixel();
  });

  // 2. Interaction Detection (Mouse, Touch, Key)
  ["click", "mousemove", "keydown", "touchstart"].forEach(evt => {
    window.addEventListener(evt, () => {
      interactions++;
      triggerSmartPixel(); 
    });
  });

  // 3. Send Internal Data to Dashboard (record.php)
  window.addEventListener("beforeunload", (e) => {
    // Don't count bots internally either (score 0 = no save)
    if (interactions === 0 && maxDepth === 0) return;

    const timeSpent = (Date.now() - start) / 1000;
    const score = Math.round((timeSpent * (maxDepth + 0.1) * (interactions + 1)) / 5);
    
    // Send data to your server
    const data = JSON.stringify({ path: location.pathname, score });
    // Ensure this path matches your folder structure
    const url = "/fair-discovery/record.php";
    
    const beaconSuccess = navigator.sendBeacon(url, data);
    if (!beaconSuccess) {
      fetch(url, { method: "POST", body: data, keepalive: true }).catch(err => console.log(err));
    }
  });

  console.log("[FairDiscovery] Smart Tracker & Pixel Initialized ✅");
})();