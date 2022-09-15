@echo off
Title Avo Assure
 
:init
set args=%*
set "started="

2>nul (
	call :start
	cd ..
)

@if "%started%"=="1" (
    echo UI Started.
	exit /b 0
) else (
	if "%started%"=="2" (
		echo Command Line execution complete.
		exit /b 0
	) else (
		echo Process aborted: "%~f0" is already running
		@ping localhost > nul
		exit /b 1
	)
)

:start
cd /d %~dp0
cd AvoAssure
if "%args%"=="" (
	9>"%~f0.lock" (
		set "started=1"
		start pythonw.exe "%cd%\plugins\core" --AVO_ASSURE_HOME "%cd%"
	)
) else (
	set "started=2"
	python.exe "%cd%\plugins\core" --AVO_ASSURE_HOME "%cd%" %args%
)
exit /b 0
