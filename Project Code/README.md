# Indigenous Health and Housing Dashboard

This project is a Streamlit dashboard based on Statistics Canada Table 41-10-0080-01 from the 2022 Indigenous Peoples Survey. It explores how housing repair needs, household crowding, and regional variation relate to self-reported general health and mental health.

## Files

- `app.py` - Streamlit dashboard
- `analysis_utils.py` - data loading, parsing, and analysis helpers
- `4110008001_databaseLoadingData.csv` - Statistics Canada data file
- `FINAL_REPORT.md` - written report

## Install

Open PowerShell in the project folder and run:

```powershell
python -m pip install -r requirements.txt
```

## Run

Start the dashboard with:

```powershell
python -m streamlit run app.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501/
```

## What The Dashboard Shows

- A national snapshot of health, repair needs, and crowding
- A regional map across provinces, territories, and broader regions
- Repair-needs charts showing how health composition changes across housing conditions
- Crowding charts showing how health composition changes across crowding levels

## Data Source

Statistics Canada, Table 41-10-0080-01:
`General health and mental health by housing situation, First Nations people living off reserve, Métis and Inuit`

Main source link:

https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=4110008001
