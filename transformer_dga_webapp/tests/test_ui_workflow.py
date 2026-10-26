"""
End-to-End Streamlit Workflow Test using Streamlit AppTest.
Tests all pages, state transitions, and user interaction flows.
"""

import unittest
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from streamlit.testing.v1 import AppTest

class TestStreamlitApp(unittest.TestCase):
    """Test full user journey using Streamlit native AppTest."""

    def test_full_user_journey(self):
        import os
        app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))
        at = AppTest.from_file(app_path, default_timeout=20)
        at.run()
        self.assertEqual(len(at.exception), 0, f"Exceptions on welcome: {at.exception}")

        # 1. Fill welcome form
        self.assertFalse(at.session_state["welcomed"])
        # Form has text_input[0] = Name, selectbox[0] = Purpose
        at.text_input[0].input("Mourya Abbadasari")
        at.selectbox[0].select("Academic learning and demonstration")
        
        # Click Continue submit button in the form
        at.button[0].click().run()
        self.assertEqual(len(at.exception), 0, f"Exceptions after welcome submit: {at.exception}")
        self.assertTrue(at.session_state["welcomed"])

        # 2. Introduction page
        self.assertFalse(at.session_state["intro_seen"])
        # Start button is the button on intro page
        at.button[0].click().run()
        self.assertEqual(len(at.exception), 0, f"Exceptions after intro: {at.exception}")
        self.assertTrue(at.session_state["intro_seen"])

        # 3. Main Dashboard overview is now active
        self.assertEqual(len(at.exception), 0)

        # 4. Navigate to New DGA Analysis
        radio = at.sidebar.radio[0]
        radio.set_value("🔬 New DGA Analysis").run()
        self.assertEqual(len(at.exception), 0, f"Exceptions on analysis page: {at.exception}")

        # Select demo sample (selectbox[1] on analysis page is demo sample selector)
        at.selectbox[1].select("Thermal fault example").run()
        self.assertEqual(len(at.exception), 0, f"Exceptions after loading demo: {at.exception}")

        # Click Analyse Transformer button
        # On analysis page, the primary button is "⚡ Analyse Transformer"
        analyse_btn = None
        for b in at.button:
            if "Analyse Transformer" in b.label:
                analyse_btn = b
                break
        self.assertIsNotNone(analyse_btn, "Analyse button not found")
        analyse_btn.click().run()
        self.assertEqual(len(at.exception), 0, f"Exceptions after running analysis: {at.exception}")

        # Verify results page rendered
        self.assertTrue(at.session_state.get("show_results"))
        last_result = at.session_state.get("last_result")
        self.assertIsNotNone(last_result)
        self.assertTrue(last_result.success)
        self.assertIn(last_result.predicted_class, ["D1", "D2", "PD", "T1", "T2", "T3"])
        print(f"Workflow test: successfully predicted {last_result.predicted_class}!")

        # Return to Dashboard
        return_btn = None
        for b in at.button:
            if "Return to Dashboard" in b.label:
                return_btn = b
                break
        self.assertIsNotNone(return_btn, "Return to Dashboard button not found")
        return_btn.click().run()
        self.assertFalse(at.session_state.get("show_results", False))

        # 5. Navigate through all remaining pages to ensure no errors
        pages_to_test = [
            "📘 DGA Knowledge Guide",
            "📖 Fault Classification Guide",
            "📈 Gas Data Visualisation",
            "🏆 Model Performance",
            "🎯 Feature Importance",
            "📋 Analysis History",
            "ℹ️ About the Project",
            "⚠️ Limitations & Safety",
            "📊 Overview",
        ]
        for page_name in pages_to_test:
            radio.set_value(page_name).run()
            self.assertEqual(len(at.exception), 0, f"Exceptions on {page_name}: {at.exception}")
            print(f"Page '{page_name}' rendered with 0 errors")


if __name__ == "__main__":
    unittest.main()
