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

$shell   = New-Object -ComObject Shell.Application
$thisPc  = $shell.Namespace(0x11)
$phone   = $thisPc.Items() | Where-Object { $_.Name -like "*Gerlyn*" }

if (-not $phone) {
    Log "ERROR: Phone not found. Make sure it is unlocked and in File Transfer (MTP) mode."
    pause
    exit
}

Log "Phone found: $($phone.Name)"

$internalStorage = $shell.Namespace($phone.Path).ParseName("Internal storage")

if (-not $internalStorage) {
    Log "ERROR: Internal storage not accessible."
    pause
    exit
}

Log "Internal storage found. Starting move to $destRoot ..."

$sourceFolder = $shell.Namespace($internalStorage.Path)
$destFolder   = $shell.Namespace($destRoot)

foreach ($item in $sourceFolder.Items()) {
    Log "Moving: $($item.Name)"
    # 0x214 = no progress dialog + yes to all + no error UI
    $destFolder.MoveHere($item, 0x214)
}

Log "=== All items queued for move. Monitor I:\ for completion. ==="
Write-Host "`nLog: $logFile"
pause