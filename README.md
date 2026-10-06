# 🔎 Reflection Mapper

### Web Parameter Reflection & Context Analysis Scanner

<p align="center">

**A lightweight Python-based security tool for discovering reflected URL parameters and identifying their reflection context.**

<br>

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](#-roadmap)
[![Security](https://img.shields.io/badge/Security-Research-red.svg)](#-responsible-use)
[![HTML Report](https://img.shields.io/badge/Reports-HTML%20%7C%20JSON-orange.svg)](#-reporting)

</p>

---

## 🚀 What is Reflection Mapper?

**Reflection Mapper** is a lightweight web security scanner designed to identify URL parameters whose values are reflected in HTTP responses.

Instead of simply reporting:

> `Parameter q is reflected`

Reflection Mapper goes one step further and attempts to determine **where the reflection occurs**.

It can currently identify contexts such as:

- `HTML_TEXT`
- `HTML_ATTRIBUTE`
- `JAVASCRIPT_STRING`
- `JAVASCRIPT`
- `JSON`
- Encoding-related reflection

It also generates structured **JSON** and human-readable **HTML security reports** containing context-specific evidence.

> ⚠️ **Reflection does not automatically mean XSS.**
>
> Reflection Mapper identifies reflection and analyzes context. It does **not** claim that every reflection is an exploitable vulnerability.

---

# ✨ Features

### 🔍 Parameter Discovery

Automatically extracts query parameters from the supplied URL.

```text
https://example.com/search?q=test&page=2
```

Detected parameters:

```text
q
page
```

---

### 🧪 Reflection Detection

Each parameter is tested using a unique marker:

```text
XSS_REFLECTION_TEST_123456
```

The scanner then checks whether the marker appears in the HTTP response.

---

### 🧠 Context Detection

Reflection Mapper attempts to determine where the marker appears.

Example:

```text
HTML_TEXT
HTML_ATTRIBUTE
JAVASCRIPT_STRING
```

This is much more useful than simply knowing that a string appeared somewhere in a response.

---

### 📌 Context-Specific Evidence

Every detected context can include its own evidence.

Example:

```text
HTML_TEXT

>Search: XSS_REFLECTION_TEST_123456<
```

```text
HTML_ATTRIBUTE

value="XSS_REFLECTION_TEST_123456"
```

```text
JAVASCRIPT_STRING

"XSS_REFLECTION_TEST_123456"
```

---

### 📊 Confidence Classification

Reflection Mapper assigns a confidence level based on the detected context.

| Confidence | Meaning |
|---|---|
| `HIGH` | Reflection found in HTML/JavaScript context |
| `MEDIUM` | Reflection detected in JSON |
| `LOW` | Reflection detected but context is uncertain |
| `NONE` | No reflection detected |

**Important:** Confidence represents the confidence of the **reflection/context analysis**, not vulnerability severity.

---

### 📄 Multiple Report Formats

Generate JSON:

```bash
python3 main.py -u "https://example.com/search?q=test" --json report.json
```

Generate HTML:

```bash
python3 main.py -u "https://example.com/search?q=test" --report report.html
```

The HTML report provides:

- Summary statistics
- Reflected parameters
- HTTP status codes
- Reflection contexts
- Confidence
- Test URLs
- Context-specific evidence

---

### ⚡ Multi-Threaded Scanning

Reflection Mapper uses Python's `ThreadPoolExecutor` to test multiple parameters concurrently.

```bash
python3 main.py \
    -u "https://example.com/search?q=test&page=1&sort=asc" \
    -t 10
```

Control concurrency with:

```text
-t / --threads
```

---

# 🧠 How It Works

Reflection Mapper follows a simple analysis pipeline:

```text
                    Target URL
                        │
                        ▼
              ┌──────────────────┐
              │ Parse URL Query  │
              │   Parameters     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Inject Unique    │
              │ Reflection Marker│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ HTTP Request     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Reflection       │
              │ Detection        │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Context Analysis │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Evidence         │
              │ Extraction       │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Confidence       │
              │ Classification   │
              └────────┬─────────┘
                       │
              ┌────────┴─────────┐
              ▼                  ▼
         JSON Report        HTML Report
```

---

# 🔬 Reflection Contexts

## HTML Text

Example:

```html
<p>Search: XSS_REFLECTION_TEST_123456</p>
```

Detected as:

```text
HTML_TEXT
```

---

## HTML Attribute

Example:

```html
<input value="XSS_REFLECTION_TEST_123456">
```

Detected as:

```text
HTML_ATTRIBUTE
```

---

## JavaScript String

Example:

```html
<script>
    const search = "XSS_REFLECTION_TEST_123456";
</script>
```

Detected as:

```text
JAVASCRIPT_STRING
```

---

## JSON

Example:

```json
{
    "search": "XSS_REFLECTION_TEST_123456"
}
```

Detected as:

```text
JSON
```

---

# 🖥️ Example

Run:

```bash
python3 main.py \
    -u "http://127.0.0.1:5000/?q=test" \
    --report test-report.html
```

Example terminal output:

```text
Target URL: http://127.0.0.1:5000/?q=test
Parameters: q
Threads: 10

[REFLECTED] q
             Context: HTML_TEXT, HTML_ATTRIBUTE, JAVASCRIPT_STRING
             Confidence: HIGH

[+] Report saved to test-report.html

[+] Scan complete
[+] Results: 1
[+] Report: test-report.html
```

---

# 📊 Example Report

The generated HTML report provides a structured view of each finding.

Example:

```text
┌─────────────────────────────────────────────┐
│             Reflection Mapper               │
│      Web Parameter Reflection Analysis      │
├─────────────────────────────────────────────┤
│                                             │
│ Parameters     Reflections     High         │
│     1               1            1           │
│                                             │
├─────────────────────────────────────────────┤
│ Finding #1                         HIGH      │
│                                             │
│ Parameter: q                                │
│ Status:    REFLECTED                        │
│ Status:    200                              │
│                                             │
│ Context:                                    │
│ [HTML_TEXT] [HTML_ATTRIBUTE]                │
│ [JAVASCRIPT_STRING]                         │
│                                             │
│ Evidence:                                   │
│                                             │
│ HTML_TEXT                                   │
│ >Search: XSS_REFLECTION_TEST_123456<        │
│                                             │
│ HTML_ATTRIBUTE                              │
│ value="XSS_REFLECTION_TEST_123456"          │
│                                             │
│ JAVASCRIPT_STRING                           │
│ "XSS_REFLECTION_TEST_123456"                │
│                                             │
└─────────────────────────────────────────────┘
```

---

# ⚙️ Installation

## Requirements

- Python 3.9+
- pip
- Internet connection for testing remote authorized targets

Clone the repository:

```bash
git clone https://github.com/akash98-ss/reflection-mapper.git
```

Enter the project:

```bash
cd reflection-mapper
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🐍 Virtual Environment

Recommended:

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Then:

```bash
pip install -r requirements.txt
```

---

# 💻 Usage

## Basic Scan

```bash
python3 main.py \
    -u "https://example.com/search?q=test"
```

Default output:

```text
report.json
```

---

## HTML Report

```bash
python3 main.py \
    -u "https://example.com/search?q=test" \
    --report report.html
```

---

## JSON Report

```bash
python3 main.py \
    -u "https://example.com/search?q=test" \
    --json report.json
```

---

## Custom Thread Count

```bash
python3 main.py \
    -u "https://example.com/search?q=test&page=1&sort=asc" \
    -t 5
```

---

## Help

```bash
python3 main.py --help
```

---

# 🧪 Local Testing Lab

Reflection Mapper includes a local Flask application that can be used to safely test reflection detection.

Start the test server:

```bash
python3 testlab/app.py
```

The server runs on:

```text
http://127.0.0.1:5000
```

Then scan:

```bash
python3 main.py \
    -u "http://127.0.0.1:5000/?q=test" \
    --report test-report.html
```

Expected result:

```text
[REFLECTED] q
Context: HTML_TEXT, HTML_ATTRIBUTE, JAVASCRIPT_STRING
Confidence: HIGH
```

This provides a controlled environment for development and testing without touching third-party systems.

---

# 🗂️ Project Structure

```text
reflection-mapper/
│
├── analyzer.py
│   └── Reflection context and evidence analysis
│
├── scanner.py
│   └── HTTP requests and parameter reflection testing
│
├── reporter.py
│   └── JSON and HTML report generation
│
├── main.py
│   └── CLI and scan orchestration
│
├── testlab/
│   └── Local reflection testing application
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Requests | HTTP communication |
| argparse | CLI interface |
| ThreadPoolExecutor | Concurrent scanning |
| Regular Expressions | Reflection/context analysis |
| Flask | Local testing lab |
| HTML/CSS | Security report |
| JSON | Structured output |

---

# 🔐 Responsible Use

Reflection Mapper is intended for:

- Security research
- Authorized penetration testing
- Bug bounty programs
- CTF environments
- Local security labs
- Application security testing
- Educational purposes

Only scan systems that you own or have explicit authorization to test.

Do not use the tool to perform unauthorized security testing against third-party systems.

**Reflection Mapper does not exploit vulnerabilities. It identifies and analyzes reflected input.**

---

# 🗺️ Roadmap

Reflection Mapper is actively being developed.

## Current

- [x] CLI interface
- [x] URL validation
- [x] Query parameter extraction
- [x] Concurrent parameter scanning
- [x] Reflection detection
- [x] HTML text detection
- [x] HTML attribute detection
- [x] JavaScript string detection
- [x] JSON detection
- [x] Evidence extraction
- [x] Confidence classification
- [x] JSON reports
- [x] HTML reports
- [x] Local testing lab

## Planned

### 🔬 Analysis

- [ ] Better HTML parsing
- [ ] Improved JavaScript context detection
- [ ] Response header analysis
- [ ] Content-Type detection
- [ ] Encoding transformation analysis
- [ ] Reflection filtering detection
- [ ] Parameter mutation analysis
- [ ] More precise evidence extraction

### 🧪 Testing

- [ ] Automated unit tests
- [ ] Integration tests
- [ ] Regression tests
- [ ] CI pipeline
- [ ] Coverage reporting

### ⚡ Scanner Improvements

- [ ] Custom headers
- [ ] Custom User-Agent
- [ ] Request timeout option
- [ ] Retry handling
- [ ] Proxy support
- [ ] Redirect controls
- [ ] Request statistics
- [ ] Verbose mode

### 📊 Reporting

- [ ] Improved severity model
- [ ] Request/response metadata
- [ ] Better evidence highlighting
- [ ] Report filtering
- [ ] Scan metadata
- [ ] Export improvements

### 🧠 Future Research

- [ ] DOM reflection analysis
- [ ] Client-side reflection detection
- [ ] Context-aware payload research
- [ ] Advanced encoding detection
- [ ] Reflection transformation tracking

---

# 🎯 Design Philosophy

Reflection Mapper follows a simple principle:

> **Detect first. Understand context second. Assess exploitability separately.**

The scanner intentionally separates:

```text
Reflection
    ↓
Context
    ↓
Evidence
    ↓
Confidence
    ↓
Potential Security Impact
```

This prevents the common mistake of treating every reflected parameter as an automatically exploitable XSS vulnerability.

---

# 📈 Why This Project?

Reflection detection is a useful building block for web application security testing.

The project was built to explore:

- HTTP request automation
- Web parameter analysis
- Reflection detection
- Context-aware security analysis
- Concurrent scanning
- Security report generation
- Python security tooling
- Automated testing

It also serves as a practical foundation for experimenting with more advanced web security analysis techniques.

---

# 🤝 Contributing

Contributions are welcome.

Typical workflow:

```bash
git clone https://github.com/akash98-ss/reflection-mapper.git

cd reflection-mapper

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a feature branch:

```bash
git checkout -b feature/improved-context-detection
```

Make your changes and test them:

```bash
python3 -m py_compile analyzer.py scanner.py reporter.py main.py
```

Commit:

```bash
git add .
git commit -m "Improve context detection"
```

Push:

```bash
git push origin feature/improved-context-detection
```

Then open a pull request.

---

# 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

**Akash Shinde**

Cyber
