/* ═══════════════════════════════════════
   ARFLOW AI — SHARED DATA & UTILITIES v2
   Uses: Teal (#0d7377) · Gold (#c9952a) · Navy (#0f1f3d)
═══════════════════════════════════════ */

const DEMO_DATA = [
  {claim_id:'C1',patient_id:'P1579',patient_age:52,patient_gender:'Female',patient_city:'Dallas',service_type:'Dental Procedure',department:'Dermatology',payer_type:'Government Medicaid',insurance_company:'None',claim_amount:13651,approved_amount:11093.05,payment_received:11093.05,balance_due:0,claim_status:'Paid',days_in_ar:7,followup_count:0,last_followup_days:11,denial_flag:0,priority_label:'Low'},
  {claim_id:'C2',patient_id:'P4906',patient_age:31,patient_gender:'Male',patient_city:'New York',service_type:'Dental Procedure',department:'Pediatrics',payer_type:'Charity Program',insurance_company:'None',claim_amount:10662,approved_amount:8576.97,payment_received:0,balance_due:8576.97,claim_status:'Pending',days_in_ar:78,followup_count:5,last_followup_days:8,denial_flag:1,priority_label:'High'},
  {claim_id:'C3',patient_id:'P6671',patient_age:48,patient_gender:'Other',patient_city:'Miami',service_type:'Health Checkup',department:'ENT',payer_type:'Charity Program',insurance_company:'None',claim_amount:12140,approved_amount:9660.40,payment_received:9660.40,balance_due:0,claim_status:'Paid',days_in_ar:17,followup_count:1,last_followup_days:1,denial_flag:1,priority_label:'Low'},
  {claim_id:'C4',patient_id:'P2341',patient_age:67,patient_gender:'Male',patient_city:'Houston',service_type:'Inpatient Surgery',department:'Cardiology',payer_type:'Blue Cross',insurance_company:'BCBS',claim_amount:18400,approved_amount:15200,payment_received:0,balance_due:15200,claim_status:'Pending',days_in_ar:95,followup_count:3,last_followup_days:12,denial_flag:1,priority_label:'High'},
  {claim_id:'C5',patient_id:'P8823',patient_age:54,patient_gender:'Female',patient_city:'Chicago',service_type:'Emergency',department:'ER',payer_type:'Aetna',insurance_company:'Aetna',claim_amount:9800,approved_amount:7200,payment_received:0,balance_due:7200,claim_status:'Denied',days_in_ar:88,followup_count:4,last_followup_days:5,denial_flag:1,priority_label:'High'},
  {claim_id:'C6',patient_id:'P3312',patient_age:43,patient_gender:'Male',patient_city:'Phoenix',service_type:'Outpatient Visit',department:'Orthopedics',payer_type:'United HC',insurance_company:'UHC',claim_amount:5600,approved_amount:4100,payment_received:0,balance_due:4100,claim_status:'In Review',days_in_ar:62,followup_count:2,last_followup_days:7,denial_flag:0,priority_label:'Medium'},
  {claim_id:'C7',patient_id:'P7765',patient_age:72,patient_gender:'Female',patient_city:'Seattle',service_type:'Radiology',department:'Radiology',payer_type:'Medicare',insurance_company:'CMS',claim_amount:3200,approved_amount:2800,payment_received:2800,balance_due:0,claim_status:'Paid',days_in_ar:10,followup_count:0,last_followup_days:20,denial_flag:0,priority_label:'Low'},
  {claim_id:'C8',patient_id:'P9901',patient_age:38,patient_gender:'Female',patient_city:'Atlanta',service_type:'Lab Tests',department:'Pathology',payer_type:'Cigna',insurance_company:'Cigna',claim_amount:1900,approved_amount:1500,payment_received:0,balance_due:1500,claim_status:'Pending',days_in_ar:45,followup_count:1,last_followup_days:15,denial_flag:0,priority_label:'Medium'},
  {claim_id:'C9',patient_id:'P4412',patient_age:61,patient_gender:'Male',patient_city:'Boston',service_type:'Inpatient',department:'Oncology',payer_type:'Humana',insurance_company:'Humana',claim_amount:22000,approved_amount:18000,payment_received:0,balance_due:18000,claim_status:'Pending',days_in_ar:80,followup_count:3,last_followup_days:9,denial_flag:1,priority_label:'High'},
  {claim_id:'C10',patient_id:'P5587',patient_age:29,patient_gender:'Male',patient_city:'Denver',service_type:'Physical Therapy',department:'Rehab',payer_type:'Medicaid',insurance_company:'None',claim_amount:4300,approved_amount:3100,payment_received:3100,balance_due:0,claim_status:'Paid',days_in_ar:22,followup_count:0,last_followup_days:30,denial_flag:0,priority_label:'Low'},
  {claim_id:'C11',patient_id:'P6634',patient_age:55,patient_gender:'Female',patient_city:'Dallas',service_type:'Mental Health',department:'Psychiatry',payer_type:'Blue Cross',insurance_company:'BCBS',claim_amount:7800,approved_amount:6200,payment_received:0,balance_due:6200,claim_status:'In Review',days_in_ar:58,followup_count:2,last_followup_days:10,denial_flag:0,priority_label:'Medium'},
  {claim_id:'C12',patient_id:'P1102',patient_age:66,patient_gender:'Male',patient_city:'Miami',service_type:'Cardiac Cath',department:'Cardiology',payer_type:'Medicare',insurance_company:'CMS',claim_amount:31000,approved_amount:25000,payment_received:0,balance_due:25000,claim_status:'Denied',days_in_ar:102,followup_count:5,last_followup_days:3,denial_flag:1,priority_label:'High'},
];

function loadData() {
  try { const s=localStorage.getItem('arflow_data'); return s?JSON.parse(s):DEMO_DATA; }
  catch(e){ return DEMO_DATA; }
}
function saveData(data){ localStorage.setItem('arflow_data',JSON.stringify(data)); }
function requireAuth(){ if(!localStorage.getItem('arflow_user')) window.location.href='login.html'; }

function money(v){ return '$'+(+v||0).toLocaleString(undefined,{minimumFractionDigits:0,maximumFractionDigits:0}); }

function prioBadge(p){
  const m={High:'b-red',Medium:'b-gold',Low:'b-teal'};
  return `<span class="badge ${m[p]||'b-gray'}">● ${p}</span>`;
}
function statusBadge(s){
  const m={Paid:'b-green',Pending:'b-gold','In Review':'b-teal',Denied:'b-red'};
  return `<span class="badge ${m[s]||'b-gray'}">${s}</span>`;
}
function ageStyle(d){
  return d>=90?'color:#dc3545;font-weight:700':d>=60?'color:#e07c1a;font-weight:700':'color:var(--muted)';
}
function riskScore(r){
  const ps={High:3,Medium:2,Low:1}[r.priority_label]||1;
  return Math.min(100,Math.round((ps/3)*55+(Math.min(r.days_in_ar||0,120)/120)*25+(Math.min(r.balance_due||0,25000)/25000)*15+(r.denial_flag||0)*5));
}
function animateCount(el,target,prefix='',suffix=''){
  if(!el) return; let n=0; const s=Math.max(1,target)/(1200/16);
  const t=setInterval(()=>{ n=Math.min(n+s,target); el.textContent=prefix+Math.floor(n).toLocaleString()+suffix; if(n>=target)clearInterval(t); },16);
}
function showToast(msg){ const t=document.getElementById('toast'); if(!t)return; t.textContent=msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),3000); }
function openModal(id){ document.getElementById(id)?.classList.add('open'); }
function closeModal(id){ document.getElementById(id)?.classList.remove('open'); }
function exportCSV(data,filename){
  if(!data||!data.length){showToast('No data to export!');return;}
  const keys=Object.keys(data[0]);
  const csv=[keys.join(','),...data.map(r=>keys.map(k=>'"'+(r[k]??'')+'"').join(','))].join('\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
  a.download=filename||'arflow_export.csv'; a.click();
  showToast('✅ CSV exported!');
}

function renderSidebar(active){
  const DATA=loadData();
  const hc=DATA.filter(d=>d.priority_label==='High'&&d.claim_status!=='Paid').length;
  const uc=DATA.filter(d=>d.claim_status!=='Paid').length;
  const user=JSON.parse(localStorage.getItem('arflow_user')||'{}');
  const initials=(user.name||'SR').split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase();
  return `<aside class="sidebar">
    <div class="sb-logo">
      <div class="sb-logo-ic">💊</div>
      <div class="sb-logo-tx">ARFlow <span>AI</span></div>
    </div>
    <div class="nav-sec">
      <div class="nav-sec-lbl">Overview</div>
      <a class="nav-it ${active==='dashboard'?'active':''}" href="dashboard.html"><span class="nav-ic">🏠</span> Dashboard</a>
      <a class="nav-it ${active==='upload'?'active':''}" href="upload.html"><span class="nav-ic">📂</span> Upload CSV</a>
      <a class="nav-it ${active==='claims'?'active':''}" href="claims.html"><span class="nav-ic">📋</span> Claims Queue <span class="nav-badge nb-red">${uc}</span></a>
    </div>
    <div class="nav-sec">
      <div class="nav-sec-lbl">Follow-Up</div>
      <a class="nav-it ${active==='tracker'?'active':''}" href="tracker.html"><span class="nav-ic">🔄</span> Follow-Up Tracker</a>
      <a class="nav-it ${active==='alerts'?'active':''}" href="alerts.html"><span class="nav-ic">🚨</span> Priority Alerts <span class="nav-badge nb-red">${hc}</span></a>
    </div>
    <div class="nav-sec">
      <div class="nav-sec-lbl">Analytics</div>
      <a class="nav-it ${active==='analytics'?'active':''}" href="analytics.html"><span class="nav-ic">📊</span> Analytics</a>
      <a class="nav-it ${active==='notifications'?'active':''}" href="notifications.html"><span class="nav-ic">🔔</span> Notifications <span class="nav-badge nb-teal">3</span></a>
    </div>
    <div class="sb-footer">
      <div class="user-row">
        <div class="ua">${initials}</div>
        <div><div class="un">${user.name||'Sarah R.'}</div><div class="ur">${user.role||'RCM Manager'}</div></div>
        <button class="logout-ic" onclick="localStorage.removeItem('arflow_user');window.location.href='login.html'" title="Logout">⏻</button>
      </div>
    </div>
  </aside>`;
}

function renderTopbar(title,sub){
  return `<div class="topbar">
    <div class="tb-left">
      <div class="pg-title">${title}</div>
      <div class="pg-sub">${sub}</div>
    </div>
    <div class="tb-right">
      <div class="ai-pill"><div class="pulse-dot"></div> AI Active</div>
      <div class="search-box" style="width:190px">
        <span style="color:var(--muted2)">🔍</span>
        <input type="text" placeholder="Search claims…" id="globalSearch" oninput="window.onGlobalSearch&&window.onGlobalSearch(this.value)"/>
      </div>
      <button class="btn btn-outline btn-sm" onclick="exportCSV(loadData(),'arflow_export.csv')">⬇ Export</button>
      <button class="btn btn-primary btn-sm" onclick="openModal('followModal')">+ Follow-Up</button>
    </div>
  </div>`;
}

function renderFollowModal(claims){
  const opts=(claims||[]).filter(d=>d.claim_status!=='Paid').map(d=>`<option>${d.claim_id} — ${d.payer_type}</option>`).join('');
  return `<div class="modal-ov" id="followModal">
    <div class="modal">
      <div class="modal-hd"><div class="modal-title">✉️ Send Follow-Up</div><button class="modal-x" onclick="closeModal('followModal')">✕</button></div>
      <div class="modal-bd">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px">
          <div><span class="ml">Claim ID</span><select class="fi">${opts}</select></div>
          <div><span class="ml">Method</span><select class="fi"><option>Email</option><option>Phone</option><option>Portal</option><option>Fax</option></select></div>
        </div>
        <span class="ml">AI-Generated Message</span>
        <textarea class="mta">Dear Payer AR Team,\n\nWe are following up on the claim which remains unpaid. Please provide an update on status and estimated payment date.\n\nThank you,\nARFlow AI — Billing Team</textarea>
        <div style="display:flex;justify-content:flex-end;gap:9px;margin-top:12px">
          <button class="btn btn-outline btn-sm" onclick="closeModal('followModal')">Cancel</button>
          <button class="btn btn-primary btn-sm" onclick="closeModal('followModal');showToast('✅ Follow-up sent!')">Send ✉️</button>
        </div>
      </div>
    </div>
  </div>`;
}

function renderToast(){ return `<div class="toast" id="toast"></div>`; }
