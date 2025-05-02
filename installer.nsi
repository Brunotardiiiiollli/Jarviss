
!define APPNAME "Jarvis Assistant"
!define VERSION "1.0"
!define COMPANY "SeuNome"
!define DESCRIPTION "Assistente de voz com GPT-4o"

Name "${APPNAME} ${VERSION}"
OutFile "JarvisSetup.exe"
InstallDir $PROGRAMFILES\Jarvis
ShowInstDetails show
ShowUnInstDetails show

Section "Main"
  SetOutPath $INSTDIR
  File /r "dist\Jarvis\*.*"

  ; criar atalho na Área de Trabalho
  CreateShortCut "$DESKTOP\Jarvis.lnk" "$INSTDIR\Jarvis.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\Jarvis.lnk"
  RMDir /r $INSTDIR
SectionEnd
