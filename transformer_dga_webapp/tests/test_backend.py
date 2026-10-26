"""
Automated Test Suite for Transformer DGA Intelligence Backend.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd

from config.settings import FEATURE_NAMES, CLASS_LABELS, DEMO_SAMPLES
from backend.model_loader import load_model, load_metadata, get_model_version
from backend.prediction import predict_transformer_fault
from backend.validation import validate_gas_inputs, validate_unit
from backend.unit_conversion import convert_to_ppm, is_unit_supported
from backend.reporting import generate_pdf_report, generate_csv_report


class TestModel(unittest.TestCase):
    """Test model loading, configuration, and inference."""

    def test_model_loading(self):
        model = load_model()
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "predict"))
        self.assertEqual(model.n_features_in_, 5)
        self.assertListEqual(sorted(model.classes_.tolist()), sorted(CLASS_LABELS))

    def test_metadata_loading(self):
        meta = load_metadata()
        self.assertIn("algorithm", meta)
        self.assertIn("feature_names", meta)
        self.assertIn("class_labels", meta)
        self.assertEqual(meta["feature_names"], FEATURE_NAMES)
        version = get_model_version()
        self.assertTrue(len(version) > 0)

    def test_demo_samples_predictions(self):
        """Verify each demo sample predicts successfully and has probabilities."""
        for name, sample_data in DEMO_SAMPLES.items():
            gases = {g: sample_data[g] for g in FEATURE_NAMES if g in sample_data}
            result = predict_transformer_fault(
                gases,
                unit="ppm",
                transformer_label=f"TEST-{name}",
                user_name="Mourya Abbadasari",
            )
            self.assertTrue(result.success, f"Failed on demo sample {name}: {result.errors}")
            self.assertIn(result.predicted_class, CLASS_LABELS)
            self.assertIn("name", result.class_description)
            self.assertEqual(len(result.probabilities), 6)
            prob_sum = sum(result.probabilities.values())
            self.assertAlmostEqual(prob_sum, 1.0, places=3)


class TestValidation(unittest.TestCase):
    """Test input validation logic."""

    def test_valid_input(self):
        sample = {"H2": 50.0, "CH4": 20.0, "C2H6": 10.0, "C2H4": 5.0, "C2H2": 1.0}
        res = validate_gas_inputs(sample)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)

    def test_missing_feature(self):
        sample = {"H2": 50.0, "CH4": 20.0}
        res = validate_gas_inputs(sample)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("C2H6" in e or "Ethane" in e for e in res.errors))

    def test_negative_values(self):
        sample = {"H2": -10.0, "CH4": 20.0, "C2H6": 10.0, "C2H4": 5.0, "C2H2": 1.0}
        res = validate_gas_inputs(sample)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Negative" in e for e in res.errors))

    def test_non_numeric_values(self):
        sample = {"H2": "abc", "CH4": 20.0, "C2H6": 10.0, "C2H4": 5.0, "C2H2": 1.0}
        res = validate_gas_inputs(sample)
        self.assertFalse(res.is_valid)

    def test_nan_values(self):
        sample = {"H2": float("nan"), "CH4": 20.0, "C2H6": 10.0, "C2H4": 5.0, "C2H2": 1.0}
        res = validate_gas_inputs(sample)
        self.assertFalse(res.is_valid)

    def test_high_value_warning(self):
        sample = {"H2": 150000.0, "CH4": 20.0, "C2H6": 10.0, "C2H4": 5.0, "C2H2": 1.0}
        res = validate_gas_inputs(sample)
        self.assertTrue(res.is_valid)
        self.assertTrue(len(res.warnings) > 0)


class TestReporting(unittest.TestCase):
    """Test PDF and CSV export generation."""

    def setUp(self):
        sample = {"H2": 100.0, "CH4": 50.0, "C2H6": 25.0, "C2H4": 10.0, "C2H2": 2.0}
        self.result = predict_transformer_fault(sample, unit="ppm", transformer_label="TX-01")

    def test_pdf_generation(self):
        pdf_bytes = generate_pdf_report(self.result)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)

    def test_csv_generation(self):
        csv_str = generate_csv_report(self.result)
        self.assertIsInstance(csv_str, str)
        self.assertIn("Transformer DGA Intelligence", csv_str)
        self.assertIn("TX-01", csv_str)
        self.assertIn(self.result.predicted_class, csv_str)


class TestUnitConversion(unittest.TestCase):
    """Test concentration unit validation and conversion."""

    def test_ppm_unit(self):
        val, success, _ = convert_to_ppm(123.4, "ppm")
        self.assertTrue(success)
        self.assertEqual(val, 123.4)

    def test_unsupported_unit(self):
        val, success, msg = convert_to_ppm(123.4, "mg/kg")
        self.assertFalse(success)
        self.assertIn("not supported", msg)


if __name__ == "__main__":
    unittest.main()
