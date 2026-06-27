$ErrorActionPreference = "Stop"

$ProjectDir = "F:\AIProjects\AgentHubControlCenter"
$TargetPath = Join-Path $ProjectDir "launch_command_center.cmd"
$ShortcutName = "AI Command Center.lnk"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath $ShortcutName

if (-not (Test-Path -LiteralPath $ProjectDir)) {
    throw "Project directory not found: $ProjectDir"
}

if (-not (Test-Path -LiteralPath $TargetPath)) {
    throw "Launcher not found: $TargetPath"
}

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $ProjectDir
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Launch AgentHubControlCenter V2 on http://localhost:8525"
$Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,220"
$Shortcut.Save()

Write-Host "Desktop shortcut updated: $ShortcutPath"
Write-Host "Target: $TargetPath"
Write-Host "Working directory: $ProjectDir"
