# ============================================================================
# Translate AI Backend - Smoke Tests Runner
# ============================================================================
# This script runs all smoke tests for the Translate AI backend services
# 
# Usage: 
#   .\run_tests_simple.ps1           # Run all tests
#   .\run_tests_simple.ps1 -stt      # Run only STT tests  
#   .\run_tests_simple.ps1 -trans    # Run only Translation tests
# ============================================================================

param(
    [switch]$stt,         # Run only STT smoke tests
    [switch]$trans,       # Run only Translation smoke tests
    [switch]$help         # Show help
)

function Show-Help {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Blue
    Write-Host " Translate AI Backend Test Runner - Help" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\run_tests_simple.ps1           # Run all smoke tests" -ForegroundColor Green
    Write-Host "  .\run_tests_simple.ps1 -stt      # Run only STT smoke tests" -ForegroundColor Green  
    Write-Host "  .\run_tests_simple.ps1 -trans    # Run only Translation smoke tests" -ForegroundColor Green
    Write-Host "  .\run_tests_simple.ps1 -help     # Show this help message" -ForegroundColor Green
    Write-Host ""
    Write-Host "Available Tests:" -ForegroundColor Yellow
    Write-Host "  * STT Service Test      - Tests Speech-to-Text with Groq API" -ForegroundColor Cyan
    Write-Host "  * Translation Test      - Tests Translation with Cohere API" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

function Test-Prerequisites {
    Write-Host ""
    Write-Host "Checking Prerequisites..." -ForegroundColor Yellow
    Write-Host "------------------------------------------------------" -ForegroundColor Yellow
    
    # Check if virtual environment exists
    if (!(Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
        Write-Host "   Please run: python -m venv .venv" -ForegroundColor Yellow
        exit 1
    }
    
    # Check if .env file exists
    if (!(Test-Path ".env")) {
        Write-Host "ERROR: .env file not found!" -ForegroundColor Red
        Write-Host "   Please create .env file with API keys" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "PASS: Virtual environment found" -ForegroundColor Green
    Write-Host "PASS: .env file found" -ForegroundColor Green
}

function Run-SmokeTest {
    param([string]$TestName, [string]$TestPath)
    
    Write-Host ""
    Write-Host "Running $TestName..." -ForegroundColor Yellow
    Write-Host "------------------------------------------------------" -ForegroundColor Yellow
    
    try {
        # Run test using the virtual environment Python
        & ".venv\Scripts\python.exe" $TestPath
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host ""
            Write-Host "PASS: $TestName PASSED" -ForegroundColor Green
            return $true
        } else {
            Write-Host ""
            Write-Host "FAIL: $TestName FAILED" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Error running $TestName : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Show-Summary {
    param([hashtable]$Results)
    
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Blue
    Write-Host " Test Results Summary" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Blue
    
    $totalTests = $Results.Count
    $passedTests = ($Results.Values | Where-Object { $_ -eq $true }).Count
    $failedTests = $totalTests - $passedTests
    
    Write-Host ""
    foreach ($testName in $Results.Keys) {
        $status = if ($Results[$testName]) { "PASS" } else { "FAIL" }
        $color = if ($Results[$testName]) { "Green" } else { "Red" }
        Write-Host "$status - $testName" -ForegroundColor $color
    }
    
    Write-Host ""
    Write-Host "Overall Results:" -ForegroundColor Yellow
    Write-Host "   Total Tests: $totalTests" -ForegroundColor Blue
    Write-Host "   Passed: $passedTests" -ForegroundColor Green  
    Write-Host "   Failed: $failedTests" -ForegroundColor $(if ($failedTests -eq 0) { "Green" } else { "Red" })
    
    if ($failedTests -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS: ALL TESTS PASSED! Backend services are ready for production!" -ForegroundColor Green
        return 0
    } else {
        Write-Host ""
        Write-Host "FAILURE: Some tests failed. Please check the output above." -ForegroundColor Red
        return 1
    }
}

# Main execution
if ($help) {
    Show-Help
}

Write-Host "======================================================================" -ForegroundColor Blue
Write-Host " Translate AI Backend - Smoke Tests Runner" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Blue

# Check prerequisites
Test-Prerequisites

# Initialize results tracking
$testResults = @{}

# Determine which tests to run
$runSTT = $stt -or (!$stt -and !$trans)  # Run STT if specifically requested or if no specific test requested
$runTranslation = $trans -or (!$stt -and !$trans)  # Run Translation if specifically requested or if no specific test requested

if ($runSTT) {
    $testResults["STT Service"] = Run-SmokeTest "STT Service Smoke Test" "tests\smoke_tests\test_stt_smoke.py"
}

if ($runTranslation) {
    $testResults["Translation Service"] = Run-SmokeTest "Translation Service Smoke Test" "tests\smoke_tests\test_translation_smoke.py"
}

# Show final summary
$exitCode = Show-Summary $testResults
Write-Host "======================================================================" -ForegroundColor Blue

exit $exitCode
