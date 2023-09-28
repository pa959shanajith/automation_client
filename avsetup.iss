; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Avo Assure Client"
#define MyAppVersion "23.1.2"
#define MyAppPublisher "AvoAutomation"
#define MyAppURL "https://www.avoautomation.ai/"
#define MyAppExeName "run.bat"


[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{1274247D-C60B-4B38-B959-0A5CA18AC771}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
VersionInfoCopyright = {#MyAppPublisher}
VersionInfoCompany = {#MyAppPublisher}

;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userappdata}\avo
DefaultGroupName=avo
DisableProgramGroupPage=yes
DisableStartupPrompt=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=..\Binaries
OutputBaseFilename=AvoAssureClient
SetupIconFile=C:\AVO\avo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableReadyPage=yes
; SignTool=ksigning /d $qAvo Assure$q /du $qhttps://www.avoautomation.ai$q $f
 

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
  

[Files]
Source: ".\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Avo\configTrial.json"; DestName:config.json;  DestDir: "{app}\Avoassure\assets"; 
;Source: "C:\Avo\updateICEConfig.ps1"; DestDir: "{app}"; 

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"   ; iconfilename:  "{app}\AvoAssure\assets\images\avo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; iconfilename:  "{app}\AvoAssure\assets\images\avo.ico"; 

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: shellexec postinstall skipifsilent

Filename: "powershell.exe";    Parameters: "-ExecutionPolicy Bypass -File ""{app}\updateICEConfig.ps1"" ""{app}"" ""{srcexe}""";   WorkingDir: {app}; 
;Flags: runhidden
   
 ;{srcexe}
 