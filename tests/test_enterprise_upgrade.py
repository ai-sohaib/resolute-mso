from __future__ import annotations

import html
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXACT = "AI-Driven Medical Billing & RCM That Stops Revenue Leakage"


class EnterpriseUpgradeTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_home_title_and_h1_are_exact_and_identical(self) -> None:
        markup = self.read("index.html")
        title = html.unescape(markup.split("<title>", 1)[1].split("</title>", 1)[0])
        h1 = html.unescape(markup.split("<h1>", 1)[1].split("</h1>", 1)[0])
        self.assertEqual(title, EXACT)
        self.assertEqual(h1, EXACT)

    def test_meta_description_requirements(self) -> None:
        markup = self.read("index.html")
        marker = '<meta name="description" content="'
        description = html.unescape(markup.split(marker, 1)[1].split('"', 1)[0])
        self.assertGreaterEqual(len(description), 150)
        self.assertLessEqual(len(description), 160)
        for term in ["U.S. healthcare providers", "medical billing", "RCM", "denials", "AR", "automation"]:
            self.assertIn(term, description)

    def test_home_cta_order(self) -> None:
        hero = self.read("index.html").split('<div class="r-hero-actions', 1)[1].split("</div>", 1)[0]
        positions = [hero.index(label) for label in ["Book a Demo", "Request a Free Audit", "Talk on WhatsApp"]]
        self.assertEqual(positions, sorted(positions))

    def test_modal_fields_and_accessibility(self) -> None:
        script = self.read("assets/js/enterprise-upgrade.js")
        for field in ["fullName","workEmail","phone","organizationName","jobTitle","organizationType","specialty","state","monthlyClaimVolume","billingSoftware","servicesOfInterest","challenge","preferredContactMethod","consent","notes"]:
            self.assertIn(field, script)
        for behavior in ["aria-modal", "Escape", "r-modal-open", "returnFocus", "aria-live", "AUDIT_SUCCESS"]:
            self.assertIn(behavior, script)
        self.assertIn("Do not submit protected health information", script)

    def test_whatsapp_is_centralized_and_safe(self) -> None:
        config = self.read("config.js")
        script = self.read("assets/js/enterprise-upgrade.js")
        css = self.read("assets/css/enterprise-upgrade.css").lower()
        self.assertIn('whatsappNumber || "17015525527"', config)
        self.assertIn('target = "_blank"', script)
        self.assertIn('rel = "noopener noreferrer"', script)
        self.assertIn("#25d366", css)
        self.assertNotIn("whatsapp-panel", self.read("index.html"))

    def test_no_client_side_form_endpoint_or_credentials(self) -> None:
        combined = "\n".join([self.read("config.js"), self.read("assets/js/source-cleanup.js"), self.read("index.html")]).lower()
        self.assertNotIn("formsubmit.co", combined)
        self.assertNotIn("smtp_password", combined)
        self.assertNotIn("resend_api_key =", combined)

    def test_worker_security_controls(self) -> None:
        worker = self.read("workers/lead-intake/src/index.js")
        for control in ["ALLOWED_ORIGINS", "FORM_RATE_LIMITER", "MAX_BODY_BYTES", "validate(data)", "possiblePhi(data)", "RESEND_API_KEY", "Cache-Control", "requestId"]:
            self.assertIn(control, worker)
        self.assertNotIn("console.log(data", worker)

    def test_postprocessor_idempotence(self) -> None:
        module_path = ROOT / "scripts/apply_enterprise_upgrade.py"
        spec = importlib.util.spec_from_file_location("upgrade", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "index.html"
            page.write_text('<html><head><title>Old</title><meta name="description" content="Old"></head><body><h1>Old</h1><a>View Automation Suite</a><form action="https://formsubmit.co/test@example.com"></form></body></html>', encoding="utf-8")
            self.assertTrue(module.process_file(page, root))
            first = page.read_text(encoding="utf-8")
            self.assertFalse(module.process_file(page, root))
            self.assertEqual(first, page.read_text(encoding="utf-8"))
            self.assertIn(EXACT, html.unescape(first))
            self.assertNotIn("formsubmit.co", first)


if __name__ == "__main__":
    unittest.main()
