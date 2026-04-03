# Indigenous Health and Housing Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Heroku](https://img.shields.io/badge/Heroku-Cloud%20Deploy-430098?logo=heroku&logoColor=white)](https://www.heroku.com/)

An end-to-end data analysis project that transforms a complex public Statistics Canada table into an interactive Streamlit dashboard exploring how housing conditions relate to self-reported general health and mental health for Indigenous populations in Canada.

This was completed as a course team project for **Data Analysis with Python (Winter 2026)** at **Algoma University**. If you are visiting this repository as part of my portfolio, the finished project lives inside **`Project Code/`**.

## Portfolio Highlights

- Parsed a messy wide-format government dataset into a reusable analytical table with Python.
- Built an interactive dashboard in Streamlit with charts, regional mapping, and guided narrative tabs.
- Used `pandas`, `matplotlib`, `seaborn`, and `pydeck` to support both exploratory analysis and presentation-ready visuals.
- Turned notebook exploration into a reproducible workflow with reusable helper functions.
- Prepared the project for cloud deployment on Heroku, including scaling and cost-control guidance.
- Produced a formal IEEE-style project paper and visual report assets.

## What This Project Shows

This project focuses on the relationship between:

- housing repair needs,
- household crowding,
- geography,
- self-reported general health,
- and self-reported mental health.

The dashboard moves from a national snapshot to regional variation and then to condition-based comparisons for repair needs and crowding. It also includes an exploration-story section showing how the analysis evolved from weekly exploratory work into the final presentation.

## Screenshots

<p align="center">
  <img src="Project%20Code/national_snapshot.png" width="48%" alt="National Snapshot dashboard view" />
  <img src="Project%20Code/regional_map.png" width="48%" alt="Regional Map dashboard view" />
</p>
<p align="center">
  <img src="Project%20Code/repair_needs_chart.png" width="48%" alt="Repair Needs and Health chart" />
  <img src="Project%20Code/crowding_chart.png" width="48%" alt="Crowding and Health chart" />
</p>

## Technical Skills Demonstrated

- Data cleaning and wrangling with `pandas`
- Parsing non-standard CSV exports into analytical datasets
- Exploratory data analysis and chart design
- Storytelling with data through dashboard structure
- Interactive app development with Streamlit
- Geographic visualization with `pydeck`
- Documentation and technical reporting
- Cloud deployment preparation with Heroku

## Repository Guide

If you want to review the finished project quickly, start here:

- Dashboard application: [`Project Code/app.py`](Project%20Code/app.py)
- Analysis helpers and parser: [`Project Code/analysis_utils.py`](Project%20Code/analysis_utils.py)
- Final paper PDF: [`Project Code/Correlation_between_general_health_and_mental_health_based_on_housing_situation_for_Indigenous_Populations.pdf`](Project%20Code/Correlation_between_general_health_and_mental_health_based_on_housing_situation_for_Indigenous_Populations.pdf)
- Overleaf/LaTeX source: [`Project Code/FINAL_REPORT_overleaf.tex`](Project%20Code/FINAL_REPORT_overleaf.tex)
- Project folder guide: [`Project Code/README.md`](Project%20Code/README.md)
- Heroku deployment guide: [`README_HEROKU.md`](README_HEROKU.md)

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Pydeck
- PowerShell
- Heroku

## Local Run

From the repository root:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run ".\Project Code\app.py"
```

## Cloud Deployment

The project was structured so it could be deployed in the cloud with Heroku. The root-level deploy files are:

- `Procfile`
- `requirements.txt`
- `runtime.txt`

The application itself remains organized under `Project Code/`, while the Heroku entry point starts the final Streamlit app from there. Deployment commands, scaling notes, and presentation-day traffic guidance are documented in [`README_HEROKU.md`](README_HEROKU.md).

## Data Source

Statistics Canada, Table 41-10-0080-01:

**General health and mental health by housing situation, First Nations people living off reserve, Metis and Inuit**

Source:
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=4110008001

## Notes

- The `assignment-*` folders are earlier course work and are not part of the final deployed dashboard.
- The finished portfolio project is the material inside `Project Code/`.
