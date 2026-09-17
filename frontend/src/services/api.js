const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export async function analyzeText(text){const r=await fetch(`${API}/api/complaints/analyze`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})}); if(!r.ok) throw new Error(await r.text()); return r.json()}
export async function analyzeFile(file){const fd=new FormData();fd.append('file',file);const r=await fetch(`${API}/api/complaints/analyze-file`,{method:'POST',body:fd});if(!r.ok)throw new Error(await r.text());return r.json()}
export async function saveComplaint(payload){const r=await fetch(`${API}/api/complaints`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok)throw new Error(await r.text());return r.json()}
export async function listComplaints(){const r=await fetch(`${API}/api/complaints`);if(!r.ok)throw new Error(await r.text());return r.json()}
