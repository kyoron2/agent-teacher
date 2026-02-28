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

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-AbsolutePath {
    param([string]$PathValue)
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $PathValue))
}

function Read-Text {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue)) { return "" }
    return [System.IO.File]::ReadAllText($PathValue)
}

function Write-Text {
    param(
        [string]$PathValue,
        [string]$Content
    )
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($PathValue, $Content, $utf8NoBom)
}

function Normalize-Text {
    param([string]$Text)
    if ([string]::IsNullOrEmpty($Text)) { return "" }
    $value = $Text.Replace("`0", "")
    $value = $value.Replace('`r`n', [Environment]::NewLine)
    $value = $value -replace "\r\n", "`n"
    $value = $value -replace "\r", "`n"
    $value = $value -replace "[ \t]+$", ""
    return ($value.Trim() + "`n")
}

function Dedup-Bullets {
    param([string]$Text)
    $seen = New-Object System.Collections.Generic.HashSet[string]
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($line in ($Text -split "`n")) {
        $trim = $line.Trim()
        if ($trim.StartsWith("- ")) {
            if ($seen.Add($trim)) { $out.Add($line) }
            continue
        }
        $out.Add($line)
    }
    return (($out -join "`n").Trim() + "`n")
}

function Get-Bullets {
    param([string]$Text)
    $items = $Text -split "`n" | Where-Object { $_.Trim().StartsWith("- ") } | ForEach-Object { $_.Trim() }
    return @($items)
}

function Ensure-ArchiveSection {
    param(
        [string]$Text,
        [string[]]$NewItems,
        [int]$MaxItems
    )
    $sectionTitle = "session-archive"
    $content = $Text
    if ($content -notmatch "(?m)^##\s*$sectionTitle\s*$") {
        $content = $content.Trim() + "`n`n## $sectionTitle`n"
    }

    $pattern = "(?ms)^##\s*$sectionTitle\s*\n(.*?)(?=^##\s|\z)"
    $m = [regex]::Match($content, $pattern)
    $existing = @()
    if ($m.Success) {
        $existing = $m.Groups[1].Value -split "`n" | Where-Object { $_.Trim().StartsWith("- ") } | ForEach-Object { $_.Trim() }
    }

    $merged = New-Object System.Collections.Generic.List[string]
    foreach ($item in ($existing + $NewItems)) {
        if ([string]::IsNullOrWhiteSpace($item)) { continue }
        if (-not $merged.Contains($item)) { $merged.Add($item) }
    }

    if ($merged.Count -gt $MaxItems) {
        $merged = [System.Collections.Generic.List[string]]($merged[($merged.Count - $MaxItems)..($merged.Count - 1)])
    }

    $replacement = "## $sectionTitle`n"
    if ($merged.Count -gt 0) {
        $replacement += ($merged -join "`n") + "`n"
    }

    if ($m.Success) {
        $prefix = $content.Substring(0, $m.Index)
        $suffix = $content.Substring($m.Index + $m.Length)
        return (($prefix + $replacement + $suffix).Trim() + "`n")
    }

    return (($content.Trim() + "`n`n" + $replacement).Trim() + "`n")
}

$shortAbs = Resolve-AbsolutePath -PathValue $ShortTermPath
$longAbs = Resolve-AbsolutePath -PathValue $LongTermPath
$sessionAbs = Resolve-AbsolutePath -PathValue $SessionPath

if (-not (Test-Path -LiteralPath $shortAbs)) { throw "Short-term memory not found: $shortAbs" }
if (-not (Test-Path -LiteralPath $longAbs)) { throw "Long-term memory not found: $longAbs" }

$shortText = Dedup-Bullets -Text (Normalize-Text -Text (Read-Text -PathValue $shortAbs))
$longText = Normalize-Text -Text (Read-Text -PathValue $longAbs)
$sessionText = Normalize-Text -Text (Read-Text -PathValue $sessionAbs)

$bullets = Get-Bullets -Text $shortText
$topItems = @()
if ($bullets.Count -gt 0) {
    $topItems = @($bullets | Select-Object -First 4)
}
else {
    $topItems = @("- no-bullets-found")
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$snapshot = @("## Session Snapshot $timestamp") + $topItems
$snapshotText = ($snapshot -join "`n").Trim()

if ([string]::IsNullOrWhiteSpace($sessionText)) {
    $sessionText = "# Session Memory (L0)`n"
}
if ($sessionText -notmatch "(?m)^#\s+Session Memory \(L0\)\s*$") {
    $sessionText = "# Session Memory (L0)`n`n" + $sessionText.Trim() + "`n"
}

# Repair malformed concatenation from previous runs: "...text.## Session Snapshot ..."
$sessionText = [regex]::Replace($sessionText, '(?m)(\S)(## Session Snapshot )', '$1' + "`n" + '$2')

$blocks = [regex]::Matches($sessionText, "(?ms)(?:^|\n)## Session Snapshot .*?(?=(?:\n## Session Snapshot )|\z)") | ForEach-Object {
    $_.Value.Trim()
}
$combined = @($blocks + $snapshotText)
if ($combined.Count -gt $MaxSessionBlocks) {
    $combined = $combined[($combined.Count - $MaxSessionBlocks)..($combined.Count - 1)]
}
$newSessionText = "# Session Memory (L0)`n`n" + (($combined -join "`n`n").Trim()) + "`n"

$archiveItems = @()
if ($Mode -eq "stage_complete") {
    foreach ($item in $topItems) {
        $archiveItems += "- [$timestamp] " + $item.TrimStart("- ").Trim()
    }
    $longText = Ensure-ArchiveSection -Text $longText -NewItems $archiveItems -MaxItems $MaxArchiveItems
}

Write-Text -PathValue $shortAbs -Content $shortText
Write-Text -PathValue $longAbs -Content $longText
Write-Text -PathValue $sessionAbs -Content $newSessionText

$result = [ordered]@{
    mode = $Mode
    updated_files = @($shortAbs, $longAbs, $sessionAbs)
    session_blocks = $combined.Count
    archived_items = $archiveItems.Count
    timestamp = $timestamp
}

Write-Output ($result | ConvertTo-Json -Depth 5)
