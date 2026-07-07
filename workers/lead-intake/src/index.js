const MAX_BODY_BYTES = 50000;
const REQUIRED = ["fullName", "workEmail", "organizationName", "consent"];
const PHI_WARNING = "Do not submit protected health information, patient information, claim data, or medical records through this public form.";

function allowedOrigins(env) {
  return (env.ALLOWED_ORIGINS || "https://www.resolutemso.com,https://resolutemso.com").split(",").map(v => v.trim()).filter(Boolean);
}

function headers(origin, env) {
  const allowed = allowedOrigins(env);
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Accept",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Cross-Origin-Resource-Policy": "same-site",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff"
  };
}

function json(body, status, origin, env) {
  return new Response(JSON.stringify(body), { status, headers: { ...headers(origin, env), "Content-Type": "application/json; charset=utf-8" } });
}

function normalize(value, max = 2000) {
  if (Array.isArray(value)) return value.map(item => normalize(item, 180)).filter(Boolean).slice(0, 30);
  return String(value ?? "").replace(/\u0000/g, "").replace(/\r\n?/g, "\n").trim().slice(0, max);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" })[c]);
}

function validEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i.test(value) && value.length <= 254;
}

function validate(data) {
  const errors = {};
  REQUIRED.forEach(field => { if (!data[field] || (field === "consent" && data[field] !== "yes")) errors[field] = "Required"; });
  if (data.workEmail && !validEmail(data.workEmail)) errors.workEmail = "Invalid email address";
  if (data.formType === "Free RCM Audit" && (!data.servicesOfInterest || ![].concat(data.servicesOfInterest).length)) errors.servicesOfInterest = "Select at least one service";
  if (Number(data.startedAt || 0) && Date.now() - Number(data.startedAt) < 2500) errors.form = "Submission was completed too quickly";
  if (data.website) errors.form = "Spam check failed";
  return errors;
}

function possiblePhi(data) {
  const text = [data.challenge, data.notes, data.message].map(v => String(v || "")).join(" ").toLowerCase();
  return [/\b(patient name|medical record|medical records|mrn|date of birth|dob|social security|ssn)\b/,/\bclaim\s*(number|#|id)\b/,/\b(member|policy)\s*(number|#|id)\b/].some(pattern => pattern.test(text));
}

async function hash(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map(byte => byte.toString(16).padStart(2, "0")).join("");
}

function rows(data) {
  const labels = {
    formType:"Form",fullName:"Full Name",workEmail:"Work Email",phone:"Phone",organizationName:"Organization",jobTitle:"Job Title",organizationType:"Organization Type",specialty:"Specialty",state:"State",monthlyClaimVolume:"Estimated Monthly Claim Volume",billingSoftware:"Current Billing or PM Software",servicesOfInterest:"Services of Interest",challenge:"Main Revenue Cycle Challenge",preferredContactMethod:"Preferred Contact Method",notes:"Notes",pageSource:"Page Source",campaign:"Campaign Parameters",submittedAt:"Submitted At"
  };
  return Object.entries(labels).filter(([key]) => data[key]).map(([key, label]) => {
    const value = Array.isArray(data[key]) ? data[key].join(", ") : data[key];
    return `<tr><th align="left" valign="top" style="padding:8px;border:1px solid #dbe3ec;background:#f5f8fb">${escapeHtml(label)}</th><td style="padding:8px;border:1px solid #dbe3ec;white-space:pre-wrap">${escapeHtml(value)}</td></tr>`;
  }).join("");
}

async function send(env, message) {
  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { "Authorization": `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(message)
  });
  if (!response.ok) throw new Error(`Email provider returned ${response.status}`);
  return response.json();
}

async function notifyTeam(env, data) {
  return send(env, {
    from: env.LEAD_FROM_EMAIL,
    to: [env.LEAD_TO_EMAIL || "support@resolutemso.com"],
    reply_to: data.workEmail,
    subject: `[Resolute MSO] ${data.formType || "Website inquiry"} — ${data.organizationName || data.fullName}`,
    html: `<div style="font-family:Arial,sans-serif;color:#132033"><h1 style="font-size:22px">New Resolute MSO website inquiry</h1><p style="padding:12px;background:#fff8dc;border-left:4px solid #9a6700"><strong>${PHI_WARNING}</strong></p><table style="border-collapse:collapse;width:100%;max-width:760px">${rows(data)}</table></div>`
  });
}

async function confirmProspect(env, data) {
  if (env.SEND_CONFIRMATION !== "true") return;
  return send(env, {
    from: env.LEAD_FROM_EMAIL,
    to: [data.workEmail],
    subject: "Resolute MSO received your request",
    html: `<div style="font-family:Arial,sans-serif;color:#132033"><p>Hello ${escapeHtml(data.fullName)},</p><p>Thank you. Your request has been received. A Resolute MSO specialist will contact you shortly.</p><p><strong>${PHI_WARNING}</strong></p><p>Resolute MSO<br>Empowering Healthcare Excellence</p></div>`
  });
}

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin") || "";
    const allowed = allowedOrigins(env);
    if (request.method === "OPTIONS") {
      if (!allowed.includes(origin)) return json({ error: "Origin not allowed" }, 403, origin, env);
      return new Response(null, { status: 204, headers: headers(origin, env) });
    }
    if (request.method !== "POST") return json({ error: "Method not allowed" }, 405, origin, env);
    if (!allowed.includes(origin)) return json({ error: "Origin not allowed" }, 403, origin, env);
    if (Number(request.headers.get("Content-Length") || 0) > MAX_BODY_BYTES) return json({ error: "Request too large" }, 413, origin, env);

    let input;
    try { input = await request.json(); } catch { return json({ error: "Invalid JSON" }, 400, origin, env); }
    const data = {};
    Object.entries(input || {}).forEach(([key, value]) => { data[key] = normalize(value); });

    if (env.FORM_RATE_LIMITER) {
      const key = await hash([request.headers.get("CF-Connecting-IP") || "unknown", String(data.workEmail || "").toLowerCase(), new URL(request.url).pathname].join("|"));
      const { success } = await env.FORM_RATE_LIMITER.limit({ key });
      if (!success) return json({ error: "Too many requests. Please try again shortly." }, 429, origin, env);
    }

    const errors = validate(data);
    if (Object.keys(errors).length) return json({ error: "Validation failed", fields: errors }, 422, origin, env);
    if (possiblePhi(data)) return json({ error: PHI_WARNING }, 422, origin, env);

    data.submittedAt = new Date().toISOString();
    data.requestId = crypto.randomUUID();
    try {
      await notifyTeam(env, data);
      ctx.waitUntil(confirmProspect(env, data).catch(error => console.error("confirmation_email_failed", { requestId:data.requestId, message:error.message })));
      return json({ ok:true, requestId:data.requestId }, 200, origin, env);
    } catch (error) {
      console.error("lead_submission_failed", { requestId:data.requestId, message:error.message });
      return json({ error:"Unable to deliver the request right now." }, 502, origin, env);
    }
  }
};
