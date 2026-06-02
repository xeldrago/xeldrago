$ErrorActionPreference = "Continue"

$destRoot = "I:\GerlynphonebackupPinkSamsung"
$logFile  = "$destRoot\move_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

function Log($msg) {
    $line = "$(Get-Date -Format 'HH:mm:ss') | $msg"
    Write-Host $line
    Add-Content -Path $logFile -Value $line
}

Log "=== Move Started ==="

$shell  = New-Object -ComObject Shell.Application
$thisPc = $shell.Namespace(0x11)
$phone  = $thisPc.Items() | Where-Object { $_.Name -like "*Gerlyn*" }

if (-not $phone) {
    Log "ERROR: Phone not found. Unlock phone and set USB to File Transfer."
    pause; exit
}

Log "Phone found: $($phone.Name)"

$phoneFolder     = $shell.Namespace($phone.Path)
$internalStorage = $phoneFolder.ParseName("Internal storage")

if (-not $internalStorage) {
    Log "ERROR: Internal storage not found."
    pause; exit
}

# KEY FIX: use .GetFolder directly instead of re-opening by path
$sourceFolder = $internalStorage.GetFolder

if (-not $sourceFolder) {
    Log "ERROR: Could not open Internal storage folder object."
    pause; exit
}

Log "Source folder opened. Item count: $($sourceFolder.Items().Count)"

$destFolder = $shell.Namespace($destRoot)

foreach ($item in $sourceFolder.Items()) {
    Log "Moving: $($item.Name)"
    $destFolder.MoveHere($item, 0x214)
    Start-Sleep -Milliseconds 500  # small gap to avoid MTP choking
}

Log "=== All items queued. Keep phone connected until I:\ stops growing. ==="
Write-Host "`nLog: $logFile"
pause