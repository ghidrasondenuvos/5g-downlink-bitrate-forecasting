<#
.SYNOPSIS
    PowerShell runner for 5G Downlink Bitrate Forecasting & Proactive Management System.
    Course: Next Generation Network Architectures, Technologies and Applications (Topic 11)
    Supervisor: Panagiotis Marantis (pmaradis@isi.gr)

.EXAMPLE
    .\run.ps1
    .\run.ps1 -Stage all
    .\run.ps1 -Stage verify
    .\run.ps1 -Stage report
#>

[CmdletBinding()]
param (
    [ValidateSet("all", "preprocess", "ml", "shap", "dl", "foundation", "prune", "proactive", "report", "presentation", "verify")]
    [string]$Stage = "all"
)

$ErrorActionPreference = "Stop"

function Write-Banner {
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "      5G DOWNLINK BITRATE FORECASTING & PROACTIVE MANAGEMENT SYSTEM           " -ForegroundColor Yellow
    Write-Host "      Course: Next Generation Network Architectures (Topic 11)                " -ForegroundColor White
    Write-Host "      Supervisor: Panagiotis Marantis (pmaradis@isi.gr)                       " -ForegroundColor Gray
    Write-Host "==============================================================================" -ForegroundColor Cyan
}

Write-Banner

switch ($Stage) {
    "all" {
        Write-Host "`n[INFO] Executing complete pipeline end-to-end..." -ForegroundColor Green
        python scripts/run_pipeline.py --all
        Write-Host "`n[INFO] Running verification test suite..." -ForegroundColor Cyan
        python scripts/verify_all.py
    }
    "verify" {
        python scripts/verify_all.py
    }
    default {
        Write-Host "`n[INFO] Executing stage: $Stage..." -ForegroundColor Green
        python scripts/run_pipeline.py --$Stage
    }
}

Write-Host "`n==============================================================================" -ForegroundColor Cyan
Write-Host "  Execution Complete! Deliverables ready in:" -ForegroundColor Green
Write-Host "    - Technical Reports: docs/Technical_Report_5G_Forecasting (.pdf, .docx, .md)" -ForegroundColor White
Write-Host "    - Presentation Deck: presentation/Downlink_Bitrate_Forecasting_5G.pptx" -ForegroundColor White
Write-Host "    - High-Res Figures:  results/figures/" -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor Cyan
