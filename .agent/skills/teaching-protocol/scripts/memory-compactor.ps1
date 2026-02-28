[CmdletBinding()]
param(
    [string]$ShortTermPath = ".agent/teaching/short_term_memory.md",
    [string]$LongTermPath = ".agent/teaching/long_term_memory.md",
    [string]$SessionPath = ".agent/teaching/session_memory.md",
    [ValidateSet("round", "stage_complete")]
    [string]$Mode = "round",
    [int]$MaxSessionBlocks = 12,
    [int]$MaxArchiveItems = 40
)

$target = Join-Path $PSScriptRoot "..\..\..\tools\memory_compactor.ps1"
if (-not (Test-Path -LiteralPath $target)) {
    throw "Target script not found: $target"
}

& $target @PSBoundParameters
