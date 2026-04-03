# Heroku Deployment Guide

This guide is for the final dashboard deployed from:

`Project Code/app.py`

## Current Deploy Structure

Heroku reads the files from the repository root:

- `Procfile`
- `requirements.txt`
- `runtime.txt`

That root `Procfile` then starts:

`Project Code/app.py`

So even though the app lives inside `Project Code`, the Heroku entry point must stay in the repository root.

## First-Time Setup

1. Install the Heroku CLI:

   https://devcenter.heroku.com/articles/heroku-cli

2. Log in:

   ```powershell
   heroku login
   ```

3. If Git complains about `dubious ownership`, mark this repo as safe:

   ```powershell
   git config --global --add safe.directory "C:/Users/Jehosua Joya/Desktop/Github Repos/data-analysis-with-python-assignments"
   ```

4. Create the Heroku app one time, or attach this repo to an existing app:

   ```powershell
   heroku create health-mental-housing
   ```

   Or, if the app already exists:

   ```powershell
   heroku git:remote -a health-mental-housing
   ```

## Deploy The Latest Dashboard

From the repository root:

```powershell
git add .
git commit -m "Deploy latest dashboard"
git push heroku main
```

If your default branch is `master`, use:

```powershell
git push heroku master
```

## Use The Control Script

This repository includes:

`scripts/heroku-dashboard.ps1`

Examples:

```powershell
.\scripts\heroku-dashboard.ps1 status
.\scripts\heroku-dashboard.ps1 up
.\scripts\heroku-dashboard.ps1 presentation
.\scripts\heroku-dashboard.ps1 down
.\scripts\heroku-dashboard.ps1 logs
```

If your Heroku app name is different:

```powershell
.\scripts\heroku-dashboard.ps1 presentation -AppName your-app-name
```

## Normal Usage

Use this when you just want the site online:

```powershell
.\scripts\heroku-dashboard.ps1 up
```

This scales the app up as:

`web=1:basic`

and opens the site in your browser.

If you prefer the personal-account sleeping tier, use:

```powershell
.\scripts\heroku-dashboard.ps1 up -Size eco
```

When you are done and want to stop paying for the running web dyno:

```powershell
.\scripts\heroku-dashboard.ps1 down
```

## Presentation Day Plan

For your presentation, where you expect around 30 simultaneous visitors, use:

```powershell
.\scripts\heroku-dashboard.ps1 presentation
```

By default, that scales the app to:

`web=2:standard-1x`

This is the recommended setup for your presentation day because:

- Heroku documents that `eco` and `basic` dynos support only one running dyno per process type.
- Heroku documents that scaling to multiple web dynos is done with `ps:scale`, for example `web=3:performance-l`.
- Heroku pricing currently lists `Standard-1X` as the first tier designed for simple horizontal scalability.

Official references:

- Dyno scaling and process limits:
  https://devcenter.heroku.com/articles/dyno-scaling-and-process-limits
- Scaling dyno formation:
  https://devcenter.heroku.com/articles/scaling
- Heroku pricing:
  https://www.heroku.com/pricing/

## Recommended Runbook For The Demo

1. Deploy your latest code the day before.
2. Turn the app on 10 to 15 minutes before the presentation:

   ```powershell
   .\scripts\heroku-dashboard.ps1 presentation
   ```

3. Open the URL and click through the main tabs once so the app is warm.
4. Keep a second terminal ready with:

   ```powershell
   .\scripts\heroku-dashboard.ps1 logs
   ```

5. If you think the audience will refresh a lot at the same time, use 3 dynos instead of 2:

   ```powershell
   .\scripts\heroku-dashboard.ps1 presentation -Dynos 3
   ```

6. When the presentation ends, turn it off:

   ```powershell
   .\scripts\heroku-dashboard.ps1 down
   ```

7. The next time you only want a cheaper single-dyno setup, use:

   ```powershell
   .\scripts\heroku-dashboard.ps1 up
   ```

   That brings the app back as `web=1:basic` instead of reusing the larger presentation formation.

## Cost Control

Scaling to zero is what stops the web dyno from running:

```powershell
heroku ps:scale web=0 -a health-mental-housing
```

This matters because Heroku's maintenance mode does not stop billing. Heroku's official documentation says maintenance mode keeps dynos running and billing hours continue to accrue.

Official reference:

https://devcenter.heroku.com/articles/maintenance-mode

## Quick Reminder

- Keep the root `Procfile`
- Deploy from the repository root
- Use `presentation` on demo day
- Use `down` when you are finished



## Automation process
Quick actions:

.\scripts\heroku-dashboard.ps1 up -AppName health-mental-housing
.\scripts\heroku-dashboard.ps1 presentation -AppName health-mental-housing
.\scripts\heroku-dashboard.ps1 down -AppName health-mental-housing
.\scripts\heroku-dashboard.ps1 logs -AppName health-mental-housing