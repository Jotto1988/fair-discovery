// fair-discovery.js - client-side aggregator
const SITES_JSON = 'sites.json';
const CACHE_KEY = 'fd_known_sites_v1';
const CACHE_TTL_MS = 1000 * 60 * 10;

async function loadSeedSites(){
  try {
    const res = await fetch(SITES_JSON + '?ts=' + Date.now());
    if(!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data.sites) ? data.sites : [];
  } catch (e) { return []; }
}

function getCachedSites(){
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if(!raw) return null;
    const parsed = JSON.parse(raw);
    if(Date.now() - parsed.ts > CACHE_TTL_MS) return null;
    return parsed.sites || [];
  } catch(e){ return null; }
}

function setCachedSites(sites){
  try { localStorage.setItem(CACHE_KEY, JSON.stringify({ts: Date.now(), sites})); } catch(e){}
}

async function discoverFeeds(seedSites){
  const known = new Set(seedSites);
  for(const feed of seedSites){
    try {
      const res = await fetch(feed + '?ts=' + Date.now());
      if(!res.ok) continue;
      const json = await res.json();
      if(json.pages && Array.isArray(json.pages)){
        json.pages.forEach(p => {
          if(typeof p.url === 'string' && p.url.includes('/fair-discovery/discovery.json')){
            try { const u = new URL(p.url, feed); known.add(u.href); } catch(e){}
          }
        });
      }
      if(json.links && Array.isArray(json.links)){
        json.links.forEach(l => {
          if(typeof l === 'string' && l.includes('/fair-discovery/discovery.json')){
            try { const u = new URL(l, feed); known.add(u.href); } catch(e){}
          }
        });
      }
    } catch(e){}
  }
  return Array.from(known);
}

async function fetchFeeds(sites){
  const merged = {};
  for(const feed of sites){
    try {
      const res = await fetch(feed + '?ts=' + Date.now());
      if(!res.ok) continue;
      const json = await res.json();
      let origin = feed;
      try { origin = (new URL(feed)).origin; } catch(e){}
      if(json.pages && Array.isArray(json.pages)){
        json.pages.forEach(p=>{
          if(!p.url || !p.score) return;
          let full = p.url;
          try { full = (new URL(p.url, origin)).href; } catch(e){ full = origin + '/' + p.url.replace(/^\/+/,''); }
          if(!merged[full]) { merged[full] = { url: full, score: 0, sites: new Set() }; }
          merged[full].score += Number(p.score);
          merged[full].sites.add(origin);
        });
      }
    } catch(e){}
  }
  return Object.values(merged).map(item => ({ url: item.url, score: item.score, sites: Array.from(item.sites) }));
}

function renderTable(list){
  const tbody = document.querySelector('#results tbody');
  tbody.innerHTML = '<tr><td colspan="2" class="small">Updating…</td></tr>';
  if(!list || list.length === 0){
    tbody.innerHTML = '<tr><td colspan="2" class="small">No data yet</td></tr>';
    return;
  }
  list.sort((a,b)=>b.score - a.score);
  const max = Math.max(...list.map(i=>i.score));
  tbody.innerHTML = '';
  list.forEach(item=>{
    const width = Math.round((item.score / (max || 1)) * 80);
    const sites = (item.sites || []).map(s=>`<span class="site">${s}</span>`).join(' ');
    const row = `<tr>
      <td><a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.url}</a>
        <div class="bar"><div class="fill" style="width:${width}%"></div></div>
        <div class="small">${sites}</div>
      </td>
      <td>${item.score}</td>
    </tr>`;
    tbody.insertAdjacentHTML('beforeend', row);
  });
  document.getElementById('status').textContent = 'Updated: ' + new Date().toLocaleString();
}

async function runAggregator(){
  document.getElementById('status').textContent = 'Loading seeds…';
  let sites = getCachedSites();
  if(!sites){
    const seeds = await loadSeedSites();
    sites = Array.isArray(seeds) ? seeds : [];
  }
  document.getElementById('status').textContent = 'Discovering…';
  const discovered = await discoverFeeds(sites.slice(0,30));
  const unique = Array.from(new Set([...sites, ...discovered])).slice(0,200);
  setCachedSites(unique);
  document.getElementById('status').textContent = 'Fetching feeds…';
  const list = await fetchFeeds(unique.slice(0,200));
  renderTable(list);
}

document.getElementById('refreshBtn').addEventListener('click', runAggregator);
document.getElementById('autoRefresh').addEventListener('change', (e)=>{
  if(e.target.checked) {
    runAggregator();
    window._fd_interval = setInterval(runAggregator, 60000);
  } else {
    clearInterval(window._fd_interval);
  }
});
document.addEventListener('DOMContentLoaded', runAggregator);
