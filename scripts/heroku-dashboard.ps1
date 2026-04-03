param(
    [Parameter(Position = 0)]
    [ValidateSet("up", "presentation", "down", "status", "logs", "open", "restart")]
    [string]$Action = "status",

    [string]$AppName = "health-mental-housing",

    [int]$Dynos = 1,

    [string]$Size = "",

    [switch]$NoOpen
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Ensure-Tool {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$InstallUrl
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "$Name is not installed. Install it first: $InstallUrl"
    }
}

function Invoke-Heroku {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & heroku @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Heroku command failed: heroku $($Arguments -join ' ')"
    }
}

function Get-ScaleTarget {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Count,

        [Parameter(Mandatory = $false)]
        [string]$DynoSize
    )

    if ([string]::IsNullOrWhiteSpace($DynoSize)) {
        return "web=$Count"
    }

    return "web=$Count`:$DynoSize"
}

Ensure-Tool -Name "heroku" -InstallUrl "https://devcenter.heroku.com/articles/heroku-cli"

switch ($Action) {
    "up" {
        if (-not $PSBoundParameters.ContainsKey("Size") -or [string]::IsNullOrWhiteSpace($Size)) {
            $Size = "basic"
        }

        $target = Get-ScaleTarget -Count $Dynos -DynoSize $Size
        Write-Host "Starting $AppName with $target ..." -ForegroundColor Cyan
        Invoke-Heroku -Arguments @("ps:scale", $target, "-a", $AppName)
        Start-Sleep -Seconds 5
        if (-not $NoOpen) {
            Invoke-Heroku -Arguments @("open", "-a", $AppName)
        }
        Write-Host "App is starting. When you finish using it, run:" -ForegroundColor Green
        Write-Host ".\scripts\heroku-dashboard.ps1 down -AppName $AppName"
        Write-Host "If you prefer a sleeping dyno on a personal account, use -Size eco instead." -ForegroundColor Yellow
    }

    "presentation" {
        if (-not $PSBoundParameters.ContainsKey("Dynos")) {
            $Dynos = 2
        }
        if (-not $PSBoundParameters.ContainsKey("Size") -or [string]::IsNullOrWhiteSpace($Size)) {
            $Size = "standard-1x"
        }

        $target = Get-ScaleTarget -Count $Dynos -DynoSize $Size
        Write-Host "Scaling $AppName for presentation traffic with $target ..." -ForegroundColor Cyan
        Invoke-Heroku -Arguments @("ps:scale", $target, "-a", $AppName)
        Start-Sleep -Seconds 5
        if (-not $NoOpen) {
            Invoke-Heroku -Arguments @("open", "-a", $AppName)
        }
        Write-Host "Recommendation: turn this on 10 to 15 minutes before the presentation and click through each tab once." -ForegroundColor Yellow
        Write-Host "If you expect heavier interaction, rerun this command with -Dynos 3." -ForegroundColor Yellow
        Write-Host "When the presentation ends, stop billing with:" -ForegroundColor Green
        Write-Host ".\scripts\heroku-dashboard.ps1 down -AppName $AppName"
    }

    "down" {
        Write-Host "Scaling $AppName down to zero ..." -ForegroundColor Cyan
        Invoke-Heroku -Arguments @("ps:scale", "web=0", "-a", $AppName)
        Write-Host "The web dyno is now at zero. That is what stops web dyno charges." -ForegroundColor Green
    }

    "status" {
        Invoke-Heroku -Arguments @("ps", "-a", $AppName)
        Write-Host ""
        Write-Host "Quick actions:" -ForegroundColor Yellow
        Write-Host ".\scripts\heroku-dashboard.ps1 up -AppName $AppName"
        Write-Host ".\scripts\heroku-dashboard.ps1 presentation -AppName $AppName"
        Write-Host ".\scripts\heroku-dashboard.ps1 down -AppName $AppName"
        Write-Host ".\scripts\heroku-dashboard.ps1 logs -AppName $AppName"
    }

    "logs" {
        Invoke-Heroku -Arguments @("logs", "--tail", "-a", $AppName)
    }

    "open" {
        Invoke-Heroku -Arguments @("open", "-a", $AppName)
    }

    "restart" {
        Invoke-Heroku -Arguments @("restart", "-a", $AppName)
        Start-Sleep -Seconds 5
        if (-not $NoOpen) {
            Invoke-Heroku -Arguments @("open", "-a", $AppName)
        }
    }
}
