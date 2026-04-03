# Indigenous Health and Housing Dashboard

This repository contains the final Streamlit dashboard for the course project and the earlier assignment folders from the same class.

## Final App

The active dashboard used for local runs and Heroku deploys is:

`Project Code/app.py`

## Files Used By Heroku

Heroku currently depends on these files:

- `Procfile`
- `requirements.txt`
- `runtime.txt`
- `Project Code/app.py`
- `Project Code/analysis_utils.py`
- `Project Code/4110008001_databaseLoadingData.csv`
- `Project Code/AUwordmark_Red-1.png`

## Guides

- Local dashboard guide: `Project Code/README.md`
- Heroku deployment guide: `README_HEROKU.md`

## Repository Notes

- The `assignment-*` folders are course history and are not part of the deployed app.
- The Heroku `Procfile` lives in the repository root on purpose. It points Heroku to `Project Code/app.py`.
