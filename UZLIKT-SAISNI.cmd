@echo off
rem Volko kalkulators - uzliek saisni uz darbvirsmas UN atver kalkulatoru.
rem Darbojas uz jebkura datora, kur ir OneDrive - VolkoEngineering (ASCII-only fails).
set KALK=%USERPROFILE%\OneDrive - VolkoEngineering\volko-kalkulators\index.html
if not exist "%KALK%" (
  echo KLUDA: nav atrasts %KALK%
  echo Parbaudi, vai OneDrive - VolkoEngineering ir sinhronizets uz si datora.
  pause
  exit /b 1
)
powershell -NoProfile -Command "$ws=New-Object -ComObject WScript.Shell; $sc=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Volko kalkulators.lnk'); $sc.TargetPath=$env:USERPROFILE+'\OneDrive - VolkoEngineering\volko-kalkulators\index.html'; $sc.Description='Volko cenas un legalizacijas cela kalkulators v2'; $sc.Save()"
echo Saisne "Volko kalkulators" uzlikta uz darbvirsmas.
start "" "%KALK%"
