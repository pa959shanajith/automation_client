@ECHO OFF

:Start
      SET /P application_name=Enter apk path or Enter 'Exit' to exit the program:
	  SET /P platform_version=Enter platform version or Enter 'Exit' to exit the program:
	  SET /P device_name=Enter device_name or Enter 'Exit' to exit the program:
	  if /I NOT "%application_name%" == "EXIT" ( if /I NOT "%platform_version%" == "EXIT" ( if /I NOT "%device_name%" == "EXIT" (
	  python android_scrapping.py %1 %application_name% %platform_version% %device_name%
	  goto Start
	  pause
	  )))
	  echo 'EXITING...'
	  choice /d y /t 1 > nul
pause 
	  

