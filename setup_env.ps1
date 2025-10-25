# LandGen Environment Setup Script (PowerShell)
# Usage: .\setup_env.ps1

Write-Host "=== LandGen Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if .env.local file exists
if (Test-Path ".env.local") {
  Write-Host "[OK] Found .env.local file, loading..." -ForegroundColor Green
    
  # Read .env.local file and set environment variables
  Get-Content ".env.local" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
      $name = $matches[1].Trim()
      $value = $matches[2].Trim()
            
      if ($name -and $value -and -not $name.StartsWith('#')) {
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
        Write-Host "  [+] Set $name" -ForegroundColor Green
      }
    }
  }
  Write-Host ""
}
else {
  Write-Host "[!] .env.local file not found" -ForegroundColor Yellow
  Write-Host ""
    
  # Prompt user for API Key
  Write-Host "Please enter your Gemini API Key:" -ForegroundColor Yellow
  Write-Host "(Get it from: https://makersuite.google.com/app/apikey)" -ForegroundColor Gray
  $geminiKey = Read-Host "GEMINI_API_KEY"
    
  if ($geminiKey) {
    [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $geminiKey, "Process")
        
    # Save to .env.local
    @"
# Google Gemini AI API Key
GEMINI_API_KEY=$geminiKey

# GitHub Personal Access Token (Optional)
# GITHUB_TOKEN=your_github_token_here
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
        
    Write-Host "[OK] Saved to .env.local" -ForegroundColor Green
  }
  Write-Host ""
    
  # Ask if user wants to set GitHub Token
  Write-Host "Do you want to set GitHub Token (optional, for higher API rate limits)? [y/N]" -ForegroundColor Yellow
  $response = Read-Host
    
  if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "(Get it from: https://github.com/settings/tokens)" -ForegroundColor Gray
    $githubToken = Read-Host "GITHUB_TOKEN"
        
    if ($githubToken) {
      [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $githubToken, "Process")
      Add-Content -Path ".env.local" -Value "`nGITHUB_TOKEN=$githubToken"
      Write-Host "[OK] Added GitHub Token" -ForegroundColor Green
    }
  }
  Write-Host ""
}

# Verify environment variables
Write-Host "=== Current Environment Status ===" -ForegroundColor Cyan

$geminiSet = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "Process")
$githubSet = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "Process")

if ($geminiSet) {
  $maskedKey = $geminiSet.Substring(0, [Math]::Min(8, $geminiSet.Length)) + "***"
  Write-Host "[OK] GEMINI_API_KEY: $maskedKey" -ForegroundColor Green
}
else {
  Write-Host "[X] GEMINI_API_KEY: Not set" -ForegroundColor Red
}

if ($githubSet) {
  $maskedToken = $githubSet.Substring(0, [Math]::Min(8, $githubSet.Length)) + "***"
  Write-Host "[OK] GITHUB_TOKEN: $maskedToken" -ForegroundColor Green
}
else {
  Write-Host "[!] GITHUB_TOKEN: Not set (optional)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "[OK] Environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Tips:" -ForegroundColor Cyan
Write-Host "  - These variables are only valid in current PowerShell session" -ForegroundColor Gray
Write-Host "  - Run '.\setup_env.ps1' again when you open a new terminal" -ForegroundColor Gray
Write-Host "  - Or manually set using: `$env:GEMINI_API_KEY = 'your_key'" -ForegroundColor Gray
Write-Host ""
