@echo off
rem Volko tiksanas klausitajs - palaid pirms tiksanas, kalkulatora 🎙 panelis pieslegsies pats.
rem ASCII-only fails (cmd.exe lauz LV diakritikas).
set PYTHONUTF8=1
python "%USERPROFILE%\OneDrive - VolkoEngineering\volko-kalkulators\scripts\meeting_listener.py" %*
pause
