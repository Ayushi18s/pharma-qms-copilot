import React,{useEffect,useState} from 'react'
import {useDispatch,useSelector} from 'react-redux'
import {Paperclip,Send,ShieldCheck,FlaskConical,Check,UserRound,AlertTriangle,Save,RefreshCw,FileText,Database,ChevronDown} from 'lucide-react'
import {setAnalysis,updateField,setSourceText,setStatus,setSaved,reset} from './store/store'
import {analyzeText,analyzeFile,saveComplaint,listComplaints} from './services/api'

const fields=[
 ['complaint_source','Complaint Source',''],['customer_name','Customer Name',''],['product_name','Product Name',''],['product_strength','Product Strength/Grade',''],['batch_number','Batch / Lot Number',''],['affected_quantity','Affected Quantity',''],['manufacturing_date','Manufacturing Date',''],['expiry_date','Expiry Date',''],['originating_site','Originating Site Block',''],['impacted_materials','Impacted Non-Product Materials (NPM)',''],['complaint_category','Complaint Category',''],['complaint_description','Complaint Description',''],['defect_summary','Structured Defect Summary','']
]
const demoText='Apollo Pharmacy reported discolored capsules in Amoxicillin Capsules 500 mg. Batch number AMX240602. Manufacturing date March 2026. Expiry date February 2028. Please log this complaint.'

function Field({name,label,value,wide=false}){const dispatch=useDispatch();return <label className={wide?'field wide':'field'}><span>{label}</span>{name==='originating_site'?<select value={value||''} onChange={e=>dispatch(updateField({key:name,value:e.target.value}))}><option value="">Awaiting AI classification...</option><option>Manufacturing</option><option>Packaging</option><option>Warehouse</option><option>Quality Control</option></select>:name==='complaint_description'||name==='defect_summary'?<textarea rows={name==='complaint_description'?4:5} value={value||''} placeholder={name==='defect_summary'?'AI will synthesize the complaint into a formal QMS description...':''} onChange={e=>dispatch(updateField({key:name,value:e.target.value}))}/>:<input value={value||''} placeholder={value?'':'Awaiting AI extraction...'} onChange={e=>dispatch(updateField({key:name,value:e.target.value}))}/>}</label>}

function App(){
 const dispatch=useDispatch(); const {form,risk,completeness,duplicate,messages,sourceText,status,savedId}=useSelector(s=>s.complaint)
 const [input,setInput]=useState(''); const [busy,setBusy]=useState(false); const [fileName,setFileName]=useState(''); const [history,setHistory]=useState([]); const [showHistory,setShowHistory]=useState(false); const [error,setError]=useState('')
 useEffect(()=>{listComplaints().then(setHistory).catch(()=>{})},[savedId])
 async function runText(){if(!input.trim())return;setBusy(true);setError('');dispatch(setSourceText(input));try{const data=await analyzeText(input);dispatch(setAnalysis({...data},{sourceText:input}));}catch(e){setError(e.message)}finally{setBusy(false)}}
 async function runFile(file){setBusy(true);setError('');setFileName(file.name);try{const data=await analyzeFile(file);dispatch(setAnalysis(data));dispatch(setSourceText(data.complaint?.complaint_description||''));}catch(e){setError(e.message)}finally{setBusy(false)}}
 async function commit(){if(!form.product_name||!form.batch_number){setError('Product and batch/lot are required before committing.');return}setBusy(true);try{const r=await saveComplaint({complaint:form,risk:risk||{},completeness:completeness||{score:0,missing_information:[]},source_text:sourceText});dispatch(setSaved(r.id))}catch(e){setError(e.message)}finally{setBusy(false)}}
 function updateChatCorrection(text){dispatch(setSourceText(sourceText+'\n'+text));setInput('');}
 return <div className="app">
  <header className="topbar"><div className="brand"><div className="brandIcon"><FlaskConical size={18}/></div><div><strong>AIVOA</strong><small>Quality Intelligence</small></div></div><div className="topActions"><button className="ghost" onClick={()=>setShowHistory(v=>!v)}><Database size={16}/> Complaint Ledger</button><button className="ghost" onClick={()=>dispatch(reset())}><RefreshCw size={16}/> New Complaint</button></div></header>
  <main className="workspace">
   <section className="formPane">
    <div className="titleRow"><div><h1>Log Customer Complaint</h1><p>API &amp; FDF Quality Assurance Module</p></div><span className={`status ${status==='Ready to Commit'?'ready':status==='Logged'?'logged':''}`}><i/> {status}</span></div>
    <div className="section"><h2>1. ORIGIN &amp; CUSTOMER DETAILS</h2><div className="grid2"><Field name="complaint_source" label="Complaint Source" value={form.complaint_source}/><Field name="customer_name" label="Customer Name" value={form.customer_name}/></div></div>
    <div className="section"><h2>2. PRODUCT &amp; BATCH IDENTIFICATION</h2><div className="grid2"><Field name="product_name" label="Product Name (API/FDF)" value={form.product_name}/><Field name="product_strength" label="Product Strength/Grade" value={form.product_strength}/><Field name="batch_number" label="Batch / Lot Number" value={form.batch_number}/><Field name="affected_quantity" label="Affected Quantity" value={form.affected_quantity}/><Field name="manufacturing_date" label="Manufacturing Date" value={form.manufacturing_date}/><Field name="expiry_date" label="Expiry Date" value={form.expiry_date}/></div></div>
    <div className="section"><h2>3. FACILITY &amp; MATERIAL IMPACT</h2><div className="grid2"><Field name="originating_site" label="Originating Site Block" value={form.originating_site}/><Field name="impacted_materials" label="Impacted Non-Product Materials (NPM)" value={form.impacted_materials}/></div></div>
    <div className="section"><h2>4. DEFECT ANALYSIS</h2><Field name="complaint_category" label="Complaint Category" value={form.complaint_category}/><Field name="complaint_description" label="Complaint Description" value={form.complaint_description} wide/><Field name="defect_summary" label="Structured Defect Summary" value={form.defect_summary} wide/>
      {risk&&<div className="riskCard"><div className="riskHead"><div><ShieldCheck size={20}/><strong>AI copilot risk assessment</strong></div><span className={`risk ${risk.risk_level?.toLowerCase()}`}>{risk.risk_level}</span></div><div className="riskGrid"><div><small>Severity (Suggested)</small><b>{risk.severity}</b></div><div><small>Risk Score</small><b>{Math.round(risk.risk_score)}/100</b></div><div><small>Confidence</small><b>{Math.round((risk.confidence||0)*100)}%</b></div><div className="wideRisk"><small>Suggested Next Action</small><b>{risk.suggested_action}</b></div></div><p className="reason">{risk.reasoning}</p><div className="recommendations"><div><strong>Root Cause Recommendation</strong><p>{risk.root_cause_recommendation}</p></div><div><strong>CAPA Recommendation</strong><p>{risk.capa_recommendation}</p></div></div></div>}
      {completeness&&<div className="complete"><div><strong>Complaint Completeness</strong><span>{Math.round(completeness.score)}%</span></div>{completeness.missing_information?.length>0?<p>Missing: {completeness.missing_information.join(', ')}</p>:<p>Required intake fields are present.</p>}</div>}
      {duplicate&&<div className="duplicate"><AlertTriangle size={18}/><div><strong>Possible duplicate detected</strong><p>{duplicate.complaint_number} — {duplicate.reason} ({Math.round(duplicate.confidence*100)}% similarity)</p></div></div>}
      <button className="commit" onClick={commit} disabled={busy||status==='Pending Triage'}><Save size={19}/> {busy?'Working…':'Commit to QMS Ledger'}</button>
      {savedId&&<div className="saved"><Check size={17}/> Complaint successfully logged as <strong>CC-2026-{String(history.length).padStart(4,'0')}</strong></div>}
    </div>
   </section>
   <aside className="copilot"><div className="copilotHead"><div><div className="copilotTitle"><FlaskConical size={19}/> AIVOA Copilot</div><p>Drop complaint files or paste text below.</p></div><span className={`online ${busy?'busy':''}`}/></div>
    <div className="chat"><div className="message ai"><div className="avatar bot"><FlaskConical size={16}/></div><div className="bubble">Ready to process new complaints. You can paste the raw email from the customer, or upload a PDF of the complaint report. I will extract the data and run the initial risk assessment.</div></div>
      {sourceText&&<div className="message user"><div className="bubble userBubble">{sourceText.split('\n')[0]}</div><div className="avatar"><UserRound size={16}/></div></div>}
      {fileName&&<div className="attachment"><FileText size={18}/><div><strong>{fileName}</strong><small>PDF / document</small></div></div>}
      {messages.map((m,i)=><div className="message ai" key={i}><div className="avatar bot"><Check size={16}/></div><div className="bubble">{m}</div></div>)}
      {busy&&<div className="message ai"><div className="avatar bot"><FlaskConical size={16}/></div><div className="bubble typing"><span/> <span/> <span/></div></div>}
      {error&&<div className="error">{error}</div>}
    </div>
    <div className="composer"><input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&runText()} placeholder="Type a message or paste a complaint…"/><label className="clip"><Paperclip size={19}/><input type="file" accept=".pdf,.txt,.eml" onChange={e=>e.target.files[0]&&runFile(e.target.files[0])}/></label><button onClick={runText} disabled={busy}><Send size={17}/></button></div><div className="powered">POWERED BY LANGGRAPH</div>
    <div className="quick"><button onClick={()=>{setInput(demoText);dispatch(setSourceText(''))}}>Load demo complaint</button><button onClick={()=>updateChatCorrection('Correction: affected quantity is 48 capsules.')}>Demo correction</button></div>
   </aside>
  </main>
  {showHistory&&<div className="drawer"><div className="drawerPanel"><div className="drawerHead"><div><h2>QMS Complaint Ledger</h2><p>Logged complaints and preliminary AI assessments</p></div><button onClick={()=>setShowHistory(false)}>×</button></div>{history.length?<div className="table">{history.map(c=><div className="row" key={c.id}><div><strong>{c.complaint_number}</strong><span>{c.product_name} · {c.batch_number}</span></div><span className={`riskPill ${c.risk_level?.toLowerCase()}`}>{c.risk_level}</span><span>{c.status}</span></div>)}</div>:<div className="empty">No complaints committed yet.</div>}</div></div>}
 </div>
}
export default App
