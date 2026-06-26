@echo off
cd /d %~dp0

:: 1. 仮想環境を有効化
call venv\Scripts\activate

:: 2. Python スクリプトを実行
python assetview_log_analyzer.py filter
python assetview_log_analyzer.py train
python assetview_log_analyzer.py analyze
python assetview_log_analyzer.py summary

pause