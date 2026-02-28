[CmdletBinding()]
param(
    [string]$ReplyFile,
    [string]$ReplyText,
    [string]$CurrentState,
    [string]$NextState
)

$target = Join-Path $PSScriptRoot "..\..\..\tools\flow_guard.ps1"
if (-not (Test-Path -LiteralPath $target)) {
    throw "Target script not found: $target"
}

& $target @PSBoundParameters
