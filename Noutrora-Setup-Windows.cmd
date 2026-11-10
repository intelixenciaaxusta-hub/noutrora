@echo off
setlocal EnableDelayedExpansion
title Instalador de Noutrora Browser v2.0 (Windows)
chcp 65001 >nul

echo ================================================================
echo   NOUTRORA BROWSER v2.0 - Instalacion automatica para Windows
echo ================================================================
echo.

set "NOUTRORA_DIR=%LOCALAPPDATA%\Noutrora"
set "FF_DIR=%NOUTRORA_DIR%\firefox"
set "PROFILE_DIR=%NOUTRORA_DIR%\profile"
set "OVERLAY_ZIP=%TEMP%\noutrora-overlay-ready.zip"
set "FF_SETUP=%TEMP%\FirefoxSetup.exe"

if not exist "%NOUTRORA_DIR%" mkdir "%NOUTRORA_DIR%"
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

if exist "%FF_DIR%\firefox.exe" goto :have_engine

if exist "%ProgramFiles%\Mozilla Firefox\firefox.exe" (
    echo [1/3] Copiando motor Gecko dende o sistema...
    xcopy "%ProgramFiles%\Mozilla Firefox\*" "%FF_DIR%\" /E /I /H /Y >nul
    goto :have_engine
)

if exist "%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe" (
    echo [1/3] Copiando motor Gecko dende o sistema...
    xcopy "%ProgramFiles(x86)%\Mozilla Firefox\*" "%FF_DIR%\" /E /I /H /Y >nul
    goto :have_engine
)

echo [1/3] Descargando motor Gecko oficial para Windows en Galego...
where curl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    curl -fL "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=gl" -o "%FF_SETUP%"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=gl', '%FF_SETUP%')"
)

if not exist "%FF_SETUP%" (
    echo [ERRO] Non se puido descargar o instalador base de Firefox.
    pause
    exit /b 1
)

echo Instalando motor base en %FF_DIR%...
start /wait "" "%FF_SETUP%" /S /InstallDirectoryPath="%FF_DIR%" /DesktopShortcut=false /StartMenuShortcut=false

:have_engine
if not exist "%FF_DIR%\firefox.exe" (
    echo [ERRO] Non se atopa o executable firefox.exe en %FF_DIR%.
    pause
    exit /b 1
)

echo [2/3] Aplicando identidade Atlantica, Bitacora e escudo de privacidade...
where curl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    curl -fsSL "https://noutrora.es/downloads/noutrora-overlay-ready.zip" -o "%OVERLAY_ZIP%"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://noutrora.es/downloads/noutrora-overlay-ready.zip', '%OVERLAY_ZIP%')"
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%OVERLAY_ZIP%' -DestinationPath '%FF_DIR%' -Force"

echo [3/3] Creando acceso directo de Noutrora no Escritorio...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $desktop = [Environment]::GetFolderPath('Desktop'); $s = $ws.CreateShortcut($desktop + '\Noutrora.lnk'); $s.TargetPath = '%FF_DIR%\firefox.exe'; $s.Arguments = '-profile ""%PROFILE_DIR%"" -no-remote'; $s.WorkingDirectory = '%FF_DIR%'; if (Test-Path '%FF_DIR%\noutrora.ico') { $s.IconLocation = '%FF_DIR%\noutrora.ico' }; $s.Description = 'Noutrora Browser'; $s.Save()"

echo.
echo ================================================================
echo   Instalacion completada con exito.
echo   Abrindo Noutrora con perfil illado...
echo ================================================================
start "" "%FF_DIR%\firefox.exe" -profile "%PROFILE_DIR%" -no-remote
