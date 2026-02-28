[CmdletBinding()]
param(
    [string]$ReplyFile,
    [string]$ReplyText,
    [string]$CurrentState,
    [string]$NextState
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Normalize-State {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    return $Value.Trim().ToUpperInvariant()
}

function Read-ReplyText {
    param(
        [string]$FilePath,
        [string]$InlineText
    )
    if (-not [string]::IsNullOrWhiteSpace($InlineText)) {
        return $InlineText
    }
    if (-not [string]::IsNullOrWhiteSpace($FilePath)) {
        if (-not (Test-Path -LiteralPath $FilePath)) {
            throw "Reply file not found: $FilePath"
        }
        return [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $FilePath).Path)
    }
    throw "Either -ReplyText or -ReplyFile is required."
}

function Extract-StateFromText {
    param([string]$Text)
    $state = ""
    $next = ""
    $stateMatch = [regex]::Match($Text, '(?im)^\s*STATE\s*=\s*([A-Z_]+)\s*$')
    if ($stateMatch.Success) {
        $state = Normalize-State $stateMatch.Groups[1].Value
    }
    $nextMatch = [regex]::Match($Text, '(?im)^\s*NEXT\s*=\s*([A-Z_]+)\s*$')
    if ($nextMatch.Success) {
        $next = Normalize-State $nextMatch.Groups[1].Value
    }
    return @{
        state = $state
        next  = $next
    }
}

function Test-BasicsCoverage {
    param([string]$Text)
    $keywordPattern = '(?i)(background|concept|syntax|principle|example|why|reason|purpose|\u80cc\u666f|\u6982\u5ff5|\u8bed\u6cd5|\u539f\u7406|\u793a\u4f8b|\u4e3a\u4ec0\u4e48|\u76ee\u7684)'
    $hits = @([regex]::Matches($Text, $keywordPattern)).Count

    $contentLines = @($Text -split "\r?\n" | Where-Object {
        $_.Trim() -ne "" -and $_ -notmatch '^\s*(STATE|NEXT|GOAL)\s*='
    }).Count
    $bulletLines = @([regex]::Matches($Text, '(?m)^\s*-\s+\S+')).Count

    return @{
        passed = ($hits -ge 3) -or ($contentLines -ge 4 -and $bulletLines -ge 2)
        hit_count = $hits
        content_lines = $contentLines
        bullet_lines = $bulletLines
    }
}

function Test-StudentAck {
    param([string]$Text)
    $ackPattern = '(?i)(understand|clear|ok to continue|ready to continue|can we continue|\u7406\u89e3|\u6e05\u695a|\u660e\u767d)'
    $questionPattern = '[\?\uFF1F]'
    return (($Text -match $ackPattern) -and ($Text -match $questionPattern))
}

function Test-RiskNotice {
    param([string]$Text)
    $riskPattern = '(?i)(risk|warning|pitfall|common mistake|attention|\u98ce\u9669|\u6ce8\u610f|\u6613\u9519|\u9677\u9631|\u5751\u70b9)'
    return ($Text -match $riskPattern)
}

$allowedTransitions = @{
    "BOOT"     = @("OVERVIEW", "EXPLAIN")
    "OVERVIEW" = @("EXPLAIN")
    "EXPLAIN"  = @("CHECK")
    "CHECK"    = @("EXPLAIN", "ACTION")
    "ACTION"   = @("VERIFY")
    "VERIFY"   = @("EXPLAIN", "CLOSE")
    "CLOSE"    = @("EXPLAIN", "OVERVIEW", "BOOT")
}

$knownStates = @("BOOT", "OVERVIEW", "EXPLAIN", "CHECK", "ACTION", "VERIFY", "CLOSE")
$guardErrors = New-Object System.Collections.Generic.List[string]
$guardWarnings = New-Object System.Collections.Generic.List[string]

$text = Read-ReplyText -FilePath $ReplyFile -InlineText $ReplyText
$extracted = Extract-StateFromText -Text $text

$current = Normalize-State $CurrentState
$next = Normalize-State $NextState

if ([string]::IsNullOrWhiteSpace($current)) { $current = $extracted.state }
if ([string]::IsNullOrWhiteSpace($next)) { $next = $extracted.next }

if ([string]::IsNullOrWhiteSpace($current) -or [string]::IsNullOrWhiteSpace($next)) {
    $guardErrors.Add("MISSING_STATE_HEADER")
}

if ($current -and ($knownStates -notcontains $current)) {
    $guardErrors.Add("UNKNOWN_STATE_$current")
}
if ($next -and ($knownStates -notcontains $next)) {
    $guardErrors.Add("UNKNOWN_NEXT_$next")
}

if ($current -and $next -and ($knownStates -contains $current) -and ($knownStates -contains $next)) {
    if ($allowedTransitions[$current] -notcontains $next) {
        $guardErrors.Add("STATE_JUMP")
    }
}

$basicEval = Test-BasicsCoverage -Text $text
$basicsCovered = [bool]$basicEval.passed
$studentAck = Test-StudentAck -Text $text
$riskNotice = Test-RiskNotice -Text $text

$hasFence = $text -match '(?ms)```.+?```'
$hasCommandLike = $text -match '(?im)^\s*(psql|python|pip|uv|npm|pnpm|yarn|docker|git|pytest|powershell)\b'
$hasSqlLike = $text -match '(?im)\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b[^`]*;'
$actionEvidence = $hasFence -or $hasCommandLike -or $hasSqlLike

if ($actionEvidence -and -not $basicsCovered) {
    $guardErrors.Add("MISS_BASICS")
}
if ($actionEvidence -and -not $studentAck) {
    $guardErrors.Add("SKIP_CHECK")
}
if ($actionEvidence -and -not $riskNotice) {
    $guardErrors.Add("MISS_RISK_NOTICE")
}

if ($next -eq "ACTION") {
    if (-not $basicsCovered) { $guardErrors.Add("GATE_BASICS_FALSE") }
    if (-not $studentAck) { $guardErrors.Add("GATE_ACK_FALSE") }
    if (-not $riskNotice) { $guardErrors.Add("GATE_RISK_FALSE") }
}

if (-not $actionEvidence -and $next -eq "ACTION") {
    $guardWarnings.Add("ACTION_WITHOUT_OPERATION_CONTENT")
}

$pass = $guardErrors.Count -eq 0
$nextAction = "ALLOW"
if (-not $pass) {
    if ($guardErrors -contains "STATE_JUMP") {
        $nextAction = "REWRITE_WITH_VALID_TRANSITION"
    }
    else {
        $nextAction = "REWRITE_FROM_EXPLAIN"
    }
}

$result = [ordered]@{
    pass = $pass
    current_state = $current
    next_state = $next
    errors = @($guardErrors)
    warnings = @($guardWarnings)
    metrics = @{
        basics_hit_count = [int]$basicEval.hit_count
        content_lines = [int]$basicEval.content_lines
        bullet_lines = [int]$basicEval.bullet_lines
        student_ack = [bool]$studentAck
        risk_notice = [bool]$riskNotice
        action_evidence = [bool]$actionEvidence
    }
    next_action = $nextAction
    checked_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

Write-Output ($result | ConvertTo-Json -Depth 6)

if (-not $pass) {
    exit 2
}
