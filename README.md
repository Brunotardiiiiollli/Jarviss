
# Jarvis Desktop App

Interface gráfica simples (Tkinter) para controlar seu assistente de voz sem precisar abrir terminal.

## Executar direto (para quem tem Python)

```bash
pip install -r requirements.txt
python jarvis_gui.py
```

## Gerar executável (Windows)

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Compile:
   ```bash
   pyinstaller --noconfirm --clean jarvis_gui.spec
   ```

3. O executável ficará em `dist/Jarvis/Jarvis.exe`.  
   Copie `.env`, `credentials.json` (Google) e tudo roda em 2 cliques.

## Gerar instalador `.exe`

*Instalador opcional* para ficar “próximo de um aplicativo comercial”:

1. Instale **NSIS**.
2. Use o script `installer.nsi` para gerar `JarvisSetup.exe`.

*(Incluímos um template de script NSIS, ajuste paths se mudar o nome.)*
