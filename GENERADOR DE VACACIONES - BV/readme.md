# 📄 HR Document Automation Tool (Python Desktop App)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-green)
![Libraries](https://img.shields.io/badge/Stack-Pandas%20%7C%20Jinja2%20%7C%20WeasyPrint%20%7C%20Tkinter-orange)

## 📌 Project Overview

This tool was designed to **automate the generation of legal HR documents** (Vacation Certificates) for large workforces. It replaces a tedious manual workflow (Excel copy-paste → Word → PDF) with a streamlined automated process, reducing processing time by **95%** and eliminating human error.

> **⚠️ Disclaimer:** This repository contains a **generalized ("sanitized") version** of a tool originally developed for a corporate environment. All sensitive data, logos, and company-specific logic have been replaced with generic placeholders (`DIV_A`, `DIV_B`, `logo_empresa.png`) for portfolio demonstration purposes.

### 🚀 Key Features

* **Bulk PDF Generation:** Processes hundreds of records from Excel to PDF in seconds.
* **Dynamic Templating:** Uses **Jinja2 + HTML/CSS** for pixel-perfect, printer-friendly documents (replacing rigid Excel layouts).
* **Business Logic:** Automatically assigns logos and checkboxes based on the employee's Division/Company entity.
* **User-Friendly GUI:** Built with **Tkinter**, featuring file selection and a non-blocking progress bar (threaded).
* **Portable Design:** Code structured to be compiled into a standalone `.exe` (using PyInstaller) for users without Python installed.

---

## 🛠️ Technical Stack

* **Core Logic:** Python 3
* **Data Processing:** `pandas` (ETL: Extraction, Transformation, Loading of Excel data).
* **Templating:** `jinja2` (Injecting dynamic context into HTML).
* **PDF Engine:** `weasyprint` (High-fidelity HTML-to-PDF conversion).
* **Concurrency:** `threading` module (Keeps the GUI responsive during heavy processing).
* **GUI:** `tkinter` (Standard Python Interface).

---

## 📂 Project Structure

```text
.
├── main.py              # Main application script (GUI + Logic)
├── template.html        # HTML Template for the document (Jinja2)
├── data_dummy.xlsx      # Sample dataset for testing
├── logo_empresa.png     # Placeholder image for the header
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
