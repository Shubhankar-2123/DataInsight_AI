# 📊 DataInsight AI – Smart Dataset Story Generator

> Transform raw datasets into meaningful business insights and AI-generated reports.

---

## 🚀 Overview

**DataInsight AI** is an AI-powered data analysis application built with **Python** and **Streamlit**. It enables users to upload datasets and automatically receive:

* Dataset overview
* Data quality assessment
* Statistical analysis
* Interactive visualizations
* Rule-based insights
* AI-generated business reports

Instead of requiring users to manually explore data, the application automatically identifies trends, anomalies, correlations, missing values, and other important findings before generating a natural-language report using a Large Language Model (LLM).

---

## ✨ Features

### 📋 Dataset Overview

* Dataset shape
* Column information
* Data types
* Memory usage
* Sample records

### 🛠 Data Quality Analysis

* Missing value detection
* Duplicate record detection
* Data completeness analysis

### 📊 Statistical Analysis

* Descriptive statistics
* Numerical summaries
* Categorical summaries

### 📈 Data Visualization

* Distribution charts
* Correlation heatmaps
* Categorical visualizations
* Time-series visualizations (when applicable)

### 💡 AI Dataset Insights

Automatically detects:

* Missing values
* Duplicate records
* Strong correlations
* Outliers
* Category distributions
* Time-series trends
* Dataset characteristics

### 🤖 AI Business Report

Generates a professional report including:

* Executive Summary
* Key Findings
* Business Insights
* Risks & Data Quality Issues
* Recommendations

---

# 🏗 Project Architecture

```text
                    CSV Dataset
                         │
                         ▼
                 Data Preprocessing
                         │
                         ▼
                Analytics Engine
              (insights.py)
                         │
                         ▼
                 Story Context
                         │
                         ▼
               Prompt Builder
                  (llm.py)
                         │
                         ▼
                Gemini AI Model
                         │
                         ▼
             AI Business Report
                         │
                         ▼
               Streamlit Interface
```

---

# 📂 Project Structure

```text
DataInsight_AI/
│
├── app.py
├── requirements.txt
├── .env
│
├── datasets/
│
├── src/
│   ├── insights.py
│   ├── llm.py
│   ├── visualization.py
│   └── utils.py
│
└── README.md
```

---

# 🛠 Tech Stack

### Programming Language

* Python

### Framework

* Streamlit

### Libraries

* Pandas
* NumPy
* Matplotlib
* Plotly

### AI

* Google Gemini API

### Environment

* python-dotenv

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/DataInsight_AI.git
```

Move into the project:

```bash
cd DataInsight_AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
streamlit run app.py
```

---

# 📌 Workflow

1. Upload a CSV dataset.
2. Explore dataset overview and quality metrics.
3. Review statistical summaries and visualizations.
4. Analyze automatically generated dataset insights.
5. Generate an AI-powered business report.

---

# 🎯 Future Improvements

* Chat with your dataset
* Export reports to PDF
* Download reports as Markdown/Word
* Dashboard generation
* Multi-file comparison
* Predictive analytics
* Automated anomaly explanations
* Natural language querying

---

# 👨‍💻 Author

**Shubhankar Sawant**

Bachelor of Engineering (Information Technology)

GitHub: https://github.com/Shubhankar-2123/DataInsight_AI

LinkedIn:https://www.linkedin.com/in/shubhankarsawant-it

---

# 📄 License

This project is licensed under the MIT License.
