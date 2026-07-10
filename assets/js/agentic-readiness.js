(() => {
  "use strict";

  const SITE = "https://www.resolutemso.com";
  const services = Object.freeze({
    "revenue cycle management": `${SITE}/revenue-cycle-management-services/`,
    "medical billing": `${SITE}/medical-billing-services/`,
    "denial management": `${SITE}/denial-management-services/`,
    "ar follow-up": `${SITE}/ar-follow-up-services/`,
    "provider enrollment": `${SITE}/provider-enrollment-services/`,
    "workflow automation": `${SITE}/healthcare-workflow-automation/`,
    "chargepilot": `${SITE}/chargepilot/`
  });

  const textResult = (text) => ({
    content: [{ type: "text", text }]
  });

  const modelContext = navigator.modelContext;
  if (!modelContext || typeof modelContext.registerTool !== "function") return;

  const registrations = [
    {
      name: "find_resolute_mso_service",
      description: "Find the most relevant Resolute MSO business service page. Do not include PHI or patient information.",
      inputSchema: {
        type: "object",
        properties: {
          need: {
            type: "string",
            description: "A business need such as medical billing, denial management, AR follow-up, provider enrollment, or workflow automation."
          }
        },
        required: ["need"],
        additionalProperties: false
      },
      execute: async ({ need }) => {
        const normalized = String(need || "").trim().toLowerCase();
        const match = Object.entries(services).find(([label]) => normalized.includes(label));
        const [label, url] = match || ["all services", `${SITE}/services/`];
        return textResult(`Recommended Resolute MSO page: ${label} — ${url}`);
      }
    },
    {
      name: "get_resolute_mso_contact",
      description: "Return Resolute MSO business contact options. This tool does not transmit form data and must not be used for PHI.",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false
      },
      execute: async () => textResult(
        "Resolute MSO business contact: support@resolutemso.com, +1 701 552 5527, WhatsApp https://wa.me/17015525527, contact page https://www.resolutemso.com/contact/. Do not submit PHI or patient information."
      )
    }
  ];

  for (const tool of registrations) {
    try {
      modelContext.registerTool(tool);
    } catch (_) {
      // Experimental implementations may reject unsupported schema fields.
      // The visible website remains fully functional without WebMCP support.
    }
  }
})();
