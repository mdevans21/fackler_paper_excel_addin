# Build script for Fackler Distributions Excel Add-in
# Run this in PowerShell on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Fackler Distributions Add-in" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check for .NET SDK
$dotnetVersion = dotnet --version 2>$null
if (-not $dotnetVersion) {
    Write-Host "ERROR: .NET SDK not found. Please install from https://dotnet.microsoft.com/download" -ForegroundColor Red
    exit 1
}
Write-Host "Using .NET SDK version: $dotnetVersion" -ForegroundColor Green

# Clean previous build
Write-Host "`nCleaning previous build..." -ForegroundColor Yellow
if (Test-Path "bin") { Remove-Item -Recurse -Force "bin" }
if (Test-Path "obj") { Remove-Item -Recurse -Force "obj" }

# Restore packages
Write-Host "`nRestoring NuGet packages..." -ForegroundColor Yellow
dotnet restore

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to restore packages" -ForegroundColor Red
    exit 1
}

# Build the project
Write-Host "`nBuilding project (Release)..." -ForegroundColor Yellow
dotnet build --configuration Release --verbosity minimal

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    exit 1
}

# Find the output
$outputDir = "bin\Release\net48"
$xllFiles = Get-ChildItem -Path $outputDir -Filter "*.xll" -ErrorAction SilentlyContinue

if ($xllFiles) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green

    Write-Host "`nGenerated files:" -ForegroundColor Cyan
    foreach ($xll in $xllFiles) {
        Write-Host "  - $($xll.Name)" -ForegroundColor White
    }

    # Create dist directory
    $distDir = "..\dist"
    if (-not (Test-Path $distDir)) {
        New-Item -ItemType Directory -Path $distDir | Out-Null
    }

    # Copy packed XLL files to dist (single-file deployment, no .dna/.dll needed)
    $publishDir = "$outputDir\publish"
    Copy-Item "$publishDir\FacklerDistributions-packed.xll" "$distDir\FacklerDistributions.xll" -Force
    Copy-Item "$publishDir\FacklerDistributions64-packed.xll" "$distDir\FacklerDistributions64.xll" -Force

    Write-Host "`nFiles copied to: $((Resolve-Path $distDir).Path)" -ForegroundColor Green

    Write-Host "`n----------------------------------------" -ForegroundColor Cyan
    Write-Host "To install in Excel:" -ForegroundColor Cyan
    Write-Host "  1. Close Excel completely" -ForegroundColor White
    Write-Host "  2. Double-click the .xll file matching your Excel:" -ForegroundColor White
    Write-Host "     - FacklerDistributions64.xll for 64-bit Excel" -ForegroundColor White
    Write-Host "     - FacklerDistributions.xll for 32-bit Excel" -ForegroundColor White
    Write-Host "  3. Click 'Enable' when prompted" -ForegroundColor White
    Write-Host "----------------------------------------" -ForegroundColor Cyan
}
else {
    Write-Host "WARNING: .xll files not found in output directory" -ForegroundColor Yellow
    Write-Host "Contents of $outputDir :" -ForegroundColor Yellow
    Get-ChildItem $outputDir -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
}
