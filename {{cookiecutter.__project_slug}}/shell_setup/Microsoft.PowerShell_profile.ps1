# Automatic .env detection
# Load .env into the current PowerShell session if present in the current directory
# --- .env loader (quiet version) --------------------------------------------
function Load-DotEnv {
    param([string]$EnvPath)

    if (-not (Test-Path $EnvPath)) { return }

    $raw   = Get-Content -Raw -LiteralPath $EnvPath -ErrorAction Stop
    $lines = $raw -split "`r?`n"

    foreach ($line in $lines) {
        if ($line -match '^\s*(#|$)') { continue }
        if ($line -match '^\s*export\s+(.*)$') { $line = $matches[1] }
        if ($line -notmatch '^\s*([^#=\s]+)\s*=\s*(.*)$') { continue }

        $name  = $matches[1].Trim() -replace '^\uFEFF','' -replace '[\u0000-\u001F]',''
        $value = $matches[2].Trim()

        if ($value.StartsWith('"') -and $value.EndsWith('"')) {
            $value = $value.Substring(1, $value.Length - 2)
        } elseif ($value.StartsWith("'") -and $value.EndsWith("'")) {
            $value = $value.Substring(1, $value.Length - 2)
        } else {
            $value = ($value -split '\s+#')[0].Trim()
        }

        [System.Environment]::SetEnvironmentVariable($name, $value, 'Process')
    }
}

try {
    $envFile = Join-Path (Get-Location).Path ".env"
    Load-DotEnv -EnvPath $envFile
    Write-Host "Loaded environment variables from .env" -ForegroundColor DarkGray
} catch {
    Write-Host "Failed to load .env: $($_.Exception.Message)" -ForegroundColor Red
}