# Desktop Launcher Guide

Status: HUB-V2-001

This guide explains how to launch AgentHubControlCenter V2 from a Windows
desktop shortcut.

## What Was Added

- `launch_command_center.cmd`
- `scripts/create_desktop_shortcut.ps1`

The launcher opens the command center at:

```text
http://localhost:8525
```

## Requirements

The launcher expects a local virtual environment inside the project folder:

```text
F:\AIProjects\AgentHubControlCenter\.venv
```

It looks for:

```text
F:\AIProjects\AgentHubControlCenter\.venv\Scripts\python.exe
F:\AIProjects\AgentHubControlCenter\.venv\Scripts\streamlit.exe
```

If neither file exists, the launcher stops with a clear error message. It does
not fall back to global Python.

## Start The Command Center

Run:

```powershell
cd F:\AIProjects\AgentHubControlCenter
.\launch_command_center.cmd
```

Expected result:

- Command window title: `AgentHubControlCenter V2`
- Streamlit starts on port `8525`
- Browser opens: `http://localhost:8525`

## Create The Desktop Shortcut

Run:

```powershell
cd F:\AIProjects\AgentHubControlCenter
powershell -ExecutionPolicy Bypass -File .\scripts\create_desktop_shortcut.ps1
```

Expected result:

- A shortcut named `AI Command Center` appears on the current Windows user's
  desktop.
- The shortcut points to `F:\AIProjects\AgentHubControlCenter\launch_command_center.cmd`.
- The shortcut working directory is `F:\AIProjects\AgentHubControlCenter`.

The script does not require administrator permission.

## Safety Boundary

The launcher and shortcut script:

- Do not read `.env`.
- Do not print API keys, tokens, credentials, or passwords.
- Do not call Gmail, Google Sheets, Notion, Airtable, Telegram, or OpenAI.
- Do not modify git remote settings.
- Do not run `git push`.

## Troubleshooting

If the launcher says no virtual environment runner was found, create or repair
the local `.venv`, then install requirements:

```powershell
cd F:\AIProjects\AgentHubControlCenter
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then run:

```powershell
.\launch_command_center.cmd
```
