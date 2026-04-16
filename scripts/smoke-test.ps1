param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$Username = "pulse_admin",
    [string]$Password = "pulse_admin",
    [switch]$CheckNegativeCases
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Invoke-JsonRequest {
    param(
        [string]$Method,
        [string]$Uri,
        [hashtable]$Headers = @{},
        [object]$Body = $null
    )

    if ($null -ne $Body) {
        return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $Headers -ContentType "application/json" -Body ($Body | ConvertTo-Json -Depth 5 -Compress)
    }

    return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $Headers
}

function Assert-ExpectedFailure {
    param(
        [scriptblock]$Request,
        [int]$ExpectedStatus,
        [string]$Label
    )

    try {
        & $Request | Out-Null
        throw "Expected $ExpectedStatus for $Label, but the request succeeded."
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -ne $ExpectedStatus) {
            throw "Expected $ExpectedStatus for $Label, got $statusCode."
        }
        Write-Host ("Expected failure confirmed: {0} -> {1}" -f $Label, $statusCode) -ForegroundColor Yellow
    }
}

Write-Step "Checking gateway health"
$health = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/health"
$health | ConvertTo-Json -Depth 5

Write-Step "Logging in"
$login = Invoke-JsonRequest -Method Post -Uri "$BaseUrl/api/auth/login" -Body @{
    username = $Username
    password = $Password
}

$token = $login.access_token
$headers = @{ Authorization = "Bearer $token" }
Write-Host "Token acquired." -ForegroundColor Green

Write-Step "Loading seed data"
$seed = Invoke-JsonRequest -Method Post -Uri "$BaseUrl/api/ingest/seed" -Headers $headers -Body @{
    clear_existing = $false
}
$seed | ConvertTo-Json -Depth 5

Write-Step "Running NLP processing"
$process = Invoke-JsonRequest -Method Post -Uri "$BaseUrl/api/process/batch" -Headers $headers -Body @{}
$process | ConvertTo-Json -Depth 5

Write-Step "Generating issues"
$issuesRun = Invoke-JsonRequest -Method Post -Uri "$BaseUrl/api/issues/auto-generate" -Headers $headers -Body @{}
$issuesRun | ConvertTo-Json -Depth 5

Write-Step "Fetching summary endpoints"
$posts = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/api/posts?page=1&page_size=5" -Headers $headers
$processed = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/api/processed?page=1&page_size=5" -Headers $headers
$trends = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/api/trends/overview" -Headers $headers
$rankings = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/api/rankings" -Headers $headers
$issues = Invoke-JsonRequest -Method Get -Uri "$BaseUrl/api/issues?page=1&page_size=5" -Headers $headers

Write-Host ""
Write-Host "Smoke test summary" -ForegroundColor Green
Write-Host ("Posts returned: {0}" -f $posts.items.Count)
Write-Host ("Processed posts returned: {0}" -f $processed.items.Count)
Write-Host ("Trend categories: {0}" -f $trends.categories.Count)
Write-Host ("Rankings returned: {0}" -f $rankings.Count)
Write-Host ("Issues returned: {0}" -f $issues.items.Count)

if ($CheckNegativeCases) {
    Write-Step "Running negative-path checks"
    Assert-ExpectedFailure -Label "unauthorized posts request" -ExpectedStatus 401 -Request {
        Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/posts?page=1&page_size=1"
    }
    Assert-ExpectedFailure -Label "unknown route" -ExpectedStatus 404 -Request {
        Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/does-not-exist" -Headers $headers
    }
    Assert-ExpectedFailure -Label "invalid login payload" -ExpectedStatus 422 -Request {
        Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/auth/login" -ContentType "application/json" -Body '{"username":"ab","password":"x"}'
    }
}
