# CloudGuard Advisor ☁️

CloudGuard Advisor is a cloud infrastructure assessment tool that helps identify **security risks, resource health issues, and cost optimization opportunities** from cloud resource data.

The project is built as a Streamlit dashboard and currently uses CSV-based resource data for assessment.

## Features

* Cloud resource health analysis
* Risk scoring for individual resources
* Security posture assessment
* Detection of publicly accessible resources
* Detection of production resources without backups
* Identification of underutilized development resources
* Cost optimization and potential savings estimation
* ROI and payback calculation
* Actionable recommendations
* Executive PDF report generation
* Interactive resource filtering and visualization
* Basic authentication for the application

## How It Works

```text
Cloud Resource Data
        ↓
Data Validation
        ↓
Resource Analysis
        ↓
Risk & Security Analysis
        ↓
Cost Optimization
        ↓
Recommendations
        ↓
ROI / Savings Analysis
        ↓
PDF Report
```

## Risk Analysis

The current version uses a simple rule-based approach to calculate resource risk.

Some of the checks include:

* Public access enabled → higher risk
* Production resource without backup → higher risk
* Development resource with very low CPU utilization → optimization opportunity

The final risk score is classified as:

| Score | Risk   |
| ----- | ------ |
| 0–39  | Low    |
| 40–59 | Medium |
| 60+   | High   |

## Cost Optimization

CloudGuard identifies potentially underutilized development resources.

For example, resources with very low CPU utilization can be flagged for:

* Right-sizing
* Scheduling
* Stopping unused resources
* Reviewing unnecessary capacity

The application also estimates potential monthly and yearly savings.

> The savings values are estimates based on the project's current rules and should not be treated as actual cloud billing data.

## Recommendations

Detected issues are converted into recommendations so that the assessment does not stop at simply showing a problem.

Examples:

* Restrict unnecessary public access
* Enable backups for production resources
* Review underutilized development resources
* Consider right-sizing or scheduling resources

## Dashboard

The Streamlit dashboard provides:

* Overall cloud health information
* Security score
* Resource risk distribution
* Cost information
* Security findings
* Resource explorer
* Cost optimization simulation
* ROI analysis
* Client action plan
* PDF report generation

## Project Structure

```text
CloudGuard-Advisor/
│
├── app.py
├── analyzer.py
├── recommendations.py
├── report_generator.py
├── requirements.txt
│
├── data/
│   └── resources.csv
│
└── README.md
```

### File Description

**`app.py`**
Main Streamlit application containing the dashboard, authentication and user interaction.

**`analyzer.py`**
Contains the main analysis logic including risk scoring, security checks, savings calculations and ROI calculations.

**`recommendations.py`**
Generates recommendations and the client action plan from identified issues.

**`report_generator.py`**
Generates the executive PDF report.

**`data/resources.csv`**
Sample cloud resource dataset used by the application.

## Technology Stack

* Python
* Streamlit
* Pandas
* Plotly
* ReportLab
* PyYAML
* Streamlit Authenticator

## Input Data

The application currently works with CSV resource data containing fields such as:

```text
resource_id
resource_name
resource_type
environment
region
cpu_utilization
memory_utilization
monthly_cost
public_access
backup_enabled
status
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/KavyanshGarg/CloudGuard-Advisor.git
cd CloudGuard-Advisor
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Cloud Architecture

The current version uses CSV data as the input source.

For a production version, the project could be extended to use Azure services such as:

* Azure Monitor
* Azure Cost Management
* Azure SQL
* Microsoft Entra ID
* Azure App Service
* Managed Identity
* RBAC

This would allow CloudGuard Advisor to work with live cloud infrastructure instead of manually uploaded data.

## What I Learned

While building this project, I worked with concepts including:

* Cloud infrastructure
* Cloud security
* Risk assessment
* Cost optimization
* Data analysis with Pandas
* Streamlit application development
* Data visualization
* Authentication
* Automated report generation
* ROI and cost-benefit analysis
* Azure cloud architecture

## Future Improvements

Some planned improvements are:

* Connect directly to Azure resources
* Use real-time Azure monitoring and cost data
* Add more security checks
* Improve risk scoring
* Add cloud compliance checks
* Add more advanced cost optimization
* Integrate AI-assisted recommendations
* Deploy the application on Azure

## Disclaimer

This project is a proof of concept. The risk scores, savings estimates and ROI calculations are based on simplified rules and sample/client-provided data.

They should not be considered a replacement for a complete cloud security audit or actual cloud billing analysis.

## Author

**Kavyansh Garg**

GitHub: [KavyanshGarg](https://github.com/KavyanshGarg)

---

⭐ If you find the project useful, consider giving it a star.
