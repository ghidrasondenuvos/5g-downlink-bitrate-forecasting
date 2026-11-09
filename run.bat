@echo off
chcp 65001 >nul
title 5G Downlink Bitrate Forecasting and Proactive Management System

echo ==============================================================================
echo       5G DOWNLINK BITRATE FORECASTING AND PROACTIVE MANAGEMENT SYSTEM
echo       Course: Next Generation Network Architectures (Topic 11)
echo       Supervisor: Panagiotis Marantis (pmaradis@isi.gr)
echo ==============================================================================
echo.

if "%1"=="--help" goto HELP
if "%1"=="-h" goto HELP
if "%1"=="midterm" goto MIDTERM
if "%1"=="verify" goto VERIFY
if "%1"=="preprocess" goto PREPROCESS
if "%1"=="ml" goto ML
if "%1"=="shap" goto SHAP
if "%1"=="dl" goto DL
if "%1"=="foundation" goto FOUNDATION
if "%1"=="prune" goto PRUNE
if "%1"=="proactive" goto PROACTIVE
if "%1"=="report" goto REPORT
if "%1"=="presentation" goto PRESENTATION

echo [INFO] Executing complete pipeline end-to-end...
python scripts\run_pipeline.py --all
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pipeline failed with error code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [INFO] Running verification test suite...
python scripts\verify_all.py
echo.
echo ==============================================================================
echo   Pipeline Execution Complete!
echo   Deliverables available at:
echo     - Technical Reports: docs\Technical_Report_5G_Forecasting (.pdf, .docx, .md)
echo     - Presentation Deck: presentation\Downlink_Bitrate_Forecasting_5G.pptx
echo     - Visualizations:   results\figures\
echo ==============================================================================
pause
exit /b 0

:MIDTERM
python scripts\run_midterm_40pct.py
exit /b 0

:PREPROCESS
python scripts\run_pipeline.py --preprocess
exit /b 0

:ML
python scripts\run_pipeline.py --ml
exit /b 0

:SHAP
python scripts\run_pipeline.py --shap
exit /b 0

:DL
python scripts\run_pipeline.py --dl
exit /b 0

:FOUNDATION
python scripts\run_pipeline.py --foundation
exit /b 0

:PRUNE
python scripts\run_pipeline.py --prune
exit /b 0

:PROACTIVE
python scripts\run_pipeline.py --proactive
exit /b 0

:REPORT
python scripts\run_pipeline.py --report
exit /b 0

:PRESENTATION
python scripts\run_pipeline.py --presentation
exit /b 0

:VERIFY
python scripts\verify_all.py
exit /b 0

:HELP
echo Usage: run.bat [option]
echo Options:
echo   midterm       Runs ONLY the 40-50%% Intermediate Phase (Preprocess + XGBoost + SHAP + Midterm Slides)
echo   (no option)   Runs complete pipeline end-to-end and verifies results
echo   verify        Runs verification test suite
echo   preprocess    Runs data cleaning, session-aware split and normalization
echo   ml            Runs XGBoost lookback and horizon grid evaluation
echo   shap          Runs TreeSHAP explainable AI analysis
echo   dl            Runs PyTorch LSTM time-series forecaster
echo   foundation    Runs IBM Granite TTM zero-shot and fine-tuning
echo   prune         Runs SHAP-guided feature pruning and latency analysis
echo   proactive     Runs 5G proactive QoS degradation early warning simulation
echo   report        Generates academic reports (.md, .docx, .pdf)
echo   presentation  Generates presentation deck (.pptx)
exit /b 0
