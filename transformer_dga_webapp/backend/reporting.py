"""
Report generation for Transformer DGA Intelligence.

Generates PDF and CSV reports from prediction results.
"""

import csv
import io
import os

from fpdf import FPDF

from config.settings import FEATURE_NAMES, FEATURE_LABELS, FEATURE_FORMULAS


def _clean_text(val):
    """Sanitize strings for Latin-1 core fonts in FPDF."""
    if val is None:
        return ""
    if not isinstance(val, str):
        val = str(val)
    replacements = {
        "₂": "2",
        "₄": "4",
        "₆": "6",
        "—": "-",
        "–": "-",
        "’": "'",
        "‘": "'",
        "”": '"',
        "“": '"',
        "°": " deg ",
        "•": "*",
        "…": "...",
        "µ": "u",
        "≤": "<=",
        "≥": ">=",
        "±": "+/-",
    }
    for k, v in replacements.items():
        val = val.replace(k, v)
    return val.encode("latin-1", "replace").decode("latin-1")


class DGAReport(FPDF):
    """Custom PDF report for DGA analysis results."""

    def cell(self, *args, **kwargs):
        if "text" in kwargs:
            kwargs["text"] = _clean_text(kwargs["text"])
        elif len(args) >= 3 and isinstance(args[2], str):
            args = list(args)
            args[2] = _clean_text(args[2])
            args = tuple(args)
        return super().cell(*args, **kwargs)

    def multi_cell(self, *args, **kwargs):
        if "text" in kwargs:
            kwargs["text"] = _clean_text(kwargs["text"])
        elif len(args) >= 3 and isinstance(args[2], str):
            args = list(args)
            args[2] = _clean_text(args[2])
            args = tuple(args)
        return super().multi_cell(*args, **kwargs)

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(20, 40, 80)
        self.cell(0, 10, "Transformer DGA Intelligence", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(
            0, 5,
            "PRML-Based Power Transformer Fault Diagnosis Using Dissolved Gas Analysis",
            new_x="LMARGIN", new_y="NEXT", align="C",
        )
        self.cell(0, 5, "Designed and developed by Mourya Abbadasari | Electrical Engineering, IIT Tirupati",
                  new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(3)
        self.set_draw_color(20, 40, 80)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(130, 130, 130)
        self.multi_cell(
            0, 3,
            "DISCLAIMER: This report records the output of an experimental "
            "machine-learning classifier. It is not a certified transformer "
            "condition assessment or a substitute for professional engineering "
            "judgement.",
            align="C",
        )
        self.set_font("Helvetica", "", 8)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")



def generate_pdf_report(prediction_result) -> bytes:
    """
    Generate a PDF report from a PredictionResult.

    Parameters
    ----------
    prediction_result : PredictionResult
        The prediction result to include in the report.

    Returns
    -------
    bytes
        The PDF content as bytes.
    """
    pdf = DGAReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)

    # ── Analysis Summary ──────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 8, "Analysis Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)

    info_items = [
        ("Reference ID", prediction_result.reference_id),
        ("Date & Time", prediction_result.timestamp),
        ("Transformer Label", prediction_result.transformer_label or "Not provided"),
        ("Analyst", prediction_result.user_name or "Not provided"),
        ("Model Version", prediction_result.model_version),
        ("Input Unit", prediction_result.input_unit),
    ]

    for label, value in info_items:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(50, 6, f"{label}:", new_x="END")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, str(value), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)

    # ── Predicted Fault Class ─────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 8, "Predicted Fault Class", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 100, 150)
    class_desc = prediction_result.class_description
    class_name = class_desc.get("name", prediction_result.predicted_class)
    pdf.cell(
        0, 8,
        f"{prediction_result.predicted_class} - {class_name}",
        new_x="LMARGIN", new_y="NEXT",
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    if "description" in class_desc:
        pdf.multi_cell(0, 5, class_desc["description"])
    pdf.ln(3)

    if "engineering_note" in class_desc:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 60, 0)
        pdf.multi_cell(0, 5, f"Engineering note: {class_desc['engineering_note']}")
    pdf.ln(5)

    # ── Gas Readings ──────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 8, "Input Gas Concentrations", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Table header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(20, 40, 80)
    pdf.set_text_color(255, 255, 255)
    col_widths = [60, 30, 45, 45]
    headers = ["Gas", "Formula", f"Value ({prediction_result.input_unit})", "Model Input (ppm)"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, border=1, fill=True, align="C", new_x="END")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)

    for gas in FEATURE_NAMES:
        input_val = prediction_result.gas_values_input.get(gas, "N/A")
        model_val = prediction_result.gas_values_model.get(gas, "N/A")
        label = FEATURE_LABELS[gas].split(" — ")[1]  # Gas name only
        formula = FEATURE_FORMULAS[gas]

        pdf.cell(col_widths[0], 6, label, border=1, new_x="END")
        pdf.cell(col_widths[1], 6, formula, border=1, align="C", new_x="END")
        pdf.cell(col_widths[2], 6, f"{float(input_val):,.2f}", border=1, align="R", new_x="END")
        pdf.cell(col_widths[3], 6, f"{float(model_val):,.2f}", border=1, align="R", new_x="END")
        pdf.ln()

    pdf.ln(5)

    # ── Probability Estimates ─────────────────────────────────────────────
    if prediction_result.probabilities:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(20, 40, 80)
        pdf.cell(0, 8, "Model-Estimated Class Probabilities", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(
            0, 4,
            "These probabilities are estimates from the Random Forest model. "
            "They should not be interpreted as calibrated diagnostic certainties."
        )
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(20, 40, 80)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(60, 7, "Fault Class", border=1, fill=True, align="C", new_x="END")
        pdf.cell(60, 7, "Estimated Probability", border=1, fill=True, align="C", new_x="END")
        pdf.ln()

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        sorted_probs = sorted(
            prediction_result.probabilities.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        for cls, prob in sorted_probs:
            pdf.cell(60, 6, cls, border=1, align="C", new_x="END")
            pdf.cell(60, 6, f"{prob:.4f} ({prob*100:.1f}%)", border=1, align="C", new_x="END")
            pdf.ln()

    pdf.ln(5)

    # ── Warnings ──────────────────────────────────────────────────────────
    if prediction_result.warnings:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(180, 120, 0)
        pdf.cell(0, 8, "Warnings", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(150, 100, 0)
        for warning in prediction_result.warnings:
            pdf.multi_cell(0, 5, f"  * {warning}")
            pdf.ln(1)

    pdf.ln(5)

    # ── Limitations ───────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 40, 80)
    pdf.cell(0, 8, "Limitations and Required Engineering Review", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(60, 60, 60)
    limitations = [
        "This prediction is generated by an experimental Random Forest classifier "
        "trained on a specific historical dataset (IEEE_STANDARD.xlsx).",
        "The model's recorded holdout accuracy is 75.42% and macro F1-score is "
        "0.7382. These metrics were measured on the evaluation dataset and do not "
        "guarantee the same performance on unseen transformers.",
        "The predicted fault class is not a confirmed physical diagnosis. It "
        "identifies a statistical pattern in the input data that resembles one "
        "of the six training categories.",
        "All DGA-based assessments should be reviewed by a qualified transformer "
        "engineer before any operational decisions are made.",
        "This application does not replace professional inspection, testing, or "
        "condition assessment procedures.",
    ]
    for lim in limitations:
        pdf.multi_cell(0, 4, f"  * {lim}")
        pdf.ln(1)

    return bytes(pdf.output())


def generate_csv_report(prediction_result) -> str:
    """
    Generate a CSV report from a PredictionResult.

    Returns
    -------
    str
        CSV content as a string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Transformer DGA Intelligence - Analysis Report"])
    writer.writerow([])

    writer.writerow(["Reference ID", prediction_result.reference_id])
    writer.writerow(["Timestamp", prediction_result.timestamp])
    writer.writerow(["Transformer Label", prediction_result.transformer_label or "Not provided"])
    writer.writerow(["Analyst", prediction_result.user_name or "Not provided"])
    writer.writerow(["Model Version", prediction_result.model_version])
    writer.writerow(["Input Unit", prediction_result.input_unit])
    writer.writerow(["Predicted Class", prediction_result.predicted_class])

    class_desc = prediction_result.class_description
    writer.writerow(["Class Name", class_desc.get("name", "")])
    writer.writerow(["Class Category", class_desc.get("category", "")])
    writer.writerow([])

    writer.writerow(["Gas Concentrations"])
    writer.writerow(["Gas", "Formula", f"Input ({prediction_result.input_unit})", "Model Input (ppm)"])
    for gas in FEATURE_NAMES:
        input_val = prediction_result.gas_values_input.get(gas, "")
        model_val = prediction_result.gas_values_model.get(gas, "")
        writer.writerow([
            FEATURE_LABELS[gas],
            FEATURE_FORMULAS[gas],
            input_val,
            model_val,
        ])

    writer.writerow([])

    if prediction_result.probabilities:
        writer.writerow(["Class Probabilities"])
        writer.writerow(["Class", "Probability"])
        for cls, prob in sorted(
            prediction_result.probabilities.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            writer.writerow([cls, f"{prob:.4f}"])

    writer.writerow([])

    if prediction_result.warnings:
        writer.writerow(["Warnings"])
        for warning in prediction_result.warnings:
            writer.writerow([warning])

    writer.writerow([])
    writer.writerow([
        "DISCLAIMER",
        "This report records the output of an experimental machine-learning "
        "classifier. It is not a certified transformer condition assessment "
        "or a substitute for professional engineering judgement.",
    ])

    return output.getvalue()
