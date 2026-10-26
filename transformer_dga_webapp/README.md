# ⚡ Transformer DGA Intelligence Platform
### *PRML-Based Power Transformer Fault Diagnosis Using Dissolved Gas Analysis*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42.0-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.6.1-F7931E.svg)](https://scikit-learn.org/)
[![IEEE C57.104](https://img.shields.io/badge/Standard-IEEE%20C57.104-00D4FF.svg)](https://standards.ieee.org/)
[![Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

> **Project Developer & Research Attribution**  
> **Mourya Abbadasari**  
> Department of Electrical Engineering, Indian Institute of Technology (IIT) Tirupati  
> *Pattern Recognition and Machine Learning (PRML) Capstone Project*

---

## 📌 Executive Summary

Power transformers are mission-critical assets in electrical transmission and distribution grids. Insulation degradation due to electrical and thermal stresses releases characteristic hydrocarbon and carbon oxide gases dissolved in transformer insulating oil (mineral oil).

This web platform bridges **academic PRML machine-learning methodologies** with **classical high-voltage power engineering standards** (IEEE C57.104 and IEC 60599). It provides utility engineers, researchers, and operators with:
1. **Machine Learning Fault Classification**: Trained Random Forest model achieving high holdout accuracy and balanced F1-scores across 6 primary transformer fault states.
2. **Classical Engineering Cross-Verification**: Duval Triangle 1 graphical ternary analysis (%CH4, %C2H4, %C2H2) running alongside ML inference to ensure diagnostic consensus.
3. **Batch Fleet Screening**: Excel/CSV multi-unit screening with automated risk categorization and fleet-wide diagnostic export.
4. **Interactive DGA Knowledge Guide**: Illustrated educational system featuring transformer internal cutaways, laboratory gas chromatography procedures, 3D molecular structures, and IEEE fault limits.
5. **Audit-Ready Reporting**: Instant downloadable PDF technical diagnostic dossiers and CSV export records.

---

## 🔬 Diagnosed Fault Classes

The diagnostic engine classifies dissolved gas concentrations into six canonical electrical and thermal fault categories:

| Fault Code | Diagnostic Description | Temperature / Energy Range | Primary Key Gases |
| :--- | :--- | :--- | :--- |
| **PD** | Partial Discharge | Low-energy discharge | Hydrogen ($H_2$), Trace Methane ($CH_4$) |
| **D1** | Low-Energy Electrical Discharge | Sparking, tracking, breakdown | Acetylene ($C_2H_2$), Hydrogen ($H_2$) |
| **D2** | High-Energy Electrical Discharge | Power arcing, flashover | High Acetylene ($C_2H_2$), Ethylene ($C_2H_4$) |
| **T1** | Thermal Fault: Low Temperature | $< 300^\circ\text{C}$ (hotspots) | Methane ($CH_4$), Ethane ($C_2H_6$) |
| **T2** | Thermal Fault: Medium Temperature | $300^\circ\text{C} - 700^\circ\text{C}$ | Ethylene ($C_2H_4$), Ethane ($C_2H_6$) |
| **T3** | Thermal Fault: High Temperature | $> 700^\circ\text{C}$ (heavy overheating) | High Ethylene ($C_2H_4$), Carbon Oxides |

---

## 🏗️ System Architecture

```text
transformer_dga_webapp/
├── run_app.bat                      # One-click Windows desktop launcher (launches server & Chrome)
├── app.py                           # Master Streamlit entry point, styling, and navigation routing
├── requirements.txt                 # Pinned dependencies
├── README.md                        # Platform engineering documentation
│
├── config/
│   ├── settings.py                  # IEEE gas definitions, thresholds, demo samples, theme tokens
│   └── model_metadata.json          # Model metrics, confusion matrix, fold scores, class mappings
│
├── models/
│   └── random_forest_model.joblib   # Trained Random Forest classifier artifact
│
├── backend/
│   ├── model_loader.py              # Model deserialization and metadata extraction
│   ├── prediction.py                # ML inference pipeline (probability distributions, consensus checks)
│   ├── validation.py                # Input hygiene (NaN, infinity, negative values, high ppm warnings)
│   ├── unit_conversion.py          # Gas concentration unit handler (ppm)
│   ├── duval.py                     # Duval Triangle 1 ternary coordinate mapping and zone classifier
│   └── reporting.py                 # FPDF2 PDF report generator and CSV exporter
│
├── views/
│   ├── welcome.py                   # Engineering onboarding and operator profile setup
│   ├── introduction.py              # Technical foundation, ML vs. classical comparison, workflow cards
│   ├── dga_guide.py                 # Illustrated knowledge guide (cutaway, GC, molecules, IEEE matrix)
│   ├── overview.py                  # Model architecture scorecard, 5-fold CV metrics, holdout comparison
│   ├── analysis.py                  # Single analysis (presets/manual) & Batch Fleet screening
│   ├── results.py                   # Badges, probability distributions, Duval Triangle plot, PDF export
│   ├── fault_guide.py               # Detailed fault compendium (PD, D1, D2, T1, T2, T3)
│   ├── model_performance.py         # Confusion matrix heatmap, precision/recall/F1 metrics
│   ├── feature_importance.py        # Permutation feature importance analysis with variance bars
│   ├── visualisation.py             # Gas distribution histograms, correlation heatmaps, box plots
│   ├── history.py                   # In-memory session diagnostic log table
│   ├── about.py                     # Academic context, PRML project background, developer credits
│   └── limitations.py               # Field safety protocols, IEEE caveats, model boundaries
│
├── assets/
│   ├── transformer_structure.jpg    # High-resolution photorealistic transformer cutaway illustration
│   └── oil_sampling_gc.jpg          # High-resolution laboratory oil sampling & GC analysis photograph
│
├── utils/
│   └── ui.py                        # Common UI elements (responsive tooltips, academic footer)
│
└── tests/
    ├── test_backend.py              # 13 automated backend unit tests (model, inference, Duval, reports)
    └── test_ui_workflow.py          # End-to-end Streamlit AppTest headless workflow test
```

---

## 🚀 Quickstart & Running the Application

### Option A: One-Click Windows Desktop Launcher (Recommended)
Double-click `run_app.bat` located in the root of the project.
This automatically:
1. Detects Python.
2. Starts the background Streamlit server on port `8501`.
3. Opens Google Chrome directly to `http://localhost:8501`.

### Option B: Terminal Command
From the project folder:
```powershell
# Activate your Python environment and run:
python -m streamlit run app.py --server.port 8501
```

### Option C: Mobile / Remote Device Access
To view and interact with the application on your mobile phone:
```powershell
# In a secondary terminal, launch an SSH tunnel:
ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=6 -R 80:localhost:8501 nokey@localhost.run
```
Open the generated HTTPS URL on any mobile browser (Safari, Chrome Mobile).  
The interface includes a dedicated mobile hamburger menu (`☰ Menu`) for seamless navigation across all 11 application modules.

---

## 🧪 Automated Testing & Verification

The platform includes full automated test coverage:

### 1. Backend Unit Tests
Validates model loading, prediction schemas, input sanitation, Duval Triangle geometry, and PDF/CSV report generation:
```powershell
python tests/test_backend.py
```
*Result: 13/13 tests passing.*

### 2. Streamlit UI End-to-End Workflow Tests
Executes headless end-to-end simulation using `streamlit.testing.v1.AppTest`, verifying user onboarding, input selection, diagnostic inference, and error-free rendering of all 11 views:
```powershell
python tests/test_ui_workflow.py
```
*Result: Ran in ~7.2s, 0 exceptions across all views.*

---

## 🛡️ Standards & References
- **IEEE Std C57.104-2019**: *IEEE Guide for the Interpretation of Gases Generated in Mineral Oil-Immersed Transformers*.
- **IEC 60599**: *Mineral oil-filled electrical equipment in service - Guidance on the interpretation of dissolved and free gases analysis*.
- **Duval, M.**: *A Review of Faults and Gas Calculation Methods in Transformers*, IEEE Electrical Insulation Magazine.
- **Scikit-Learn**: *Random Forest Classifiers & Permutation Feature Importance*.

---

## 👨‍💻 Author & Acknowledgments
- **Developer**: Mourya Abbadasari
- **Institution**: Department of Electrical Engineering, Indian Institute of Technology (IIT) Tirupati
- **Course**: Pattern Recognition and Machine Learning (PRML)
