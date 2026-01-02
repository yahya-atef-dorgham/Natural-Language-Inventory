# OpenAI API Key Setup Script for Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenAI GPT Integration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env already exists
$envPath = "backend\.env"
if (Test-Path $envPath) {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Setup cancelled." -ForegroundColor Red
        exit
    }
}

Write-Host ""
Write-Host "📝 Please provide your OpenAI API key" -ForegroundColor Green
Write-Host "   Get one at: https://platform.openai.com/api-keys" -ForegroundColor Gray
Write-Host ""

# Prompt for API key
$apiKey = Read-Host "Enter your OpenAI API key"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "❌ API key cannot be empty!" -ForegroundColor Red
    exit 1
}

# Validate API key format (basic check)
if (-not $apiKey.StartsWith("sk-")) {
    Write-Host "⚠️  Warning: API key should start with 'sk-'" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Setup cancelled." -ForegroundColor Red
        exit
    }
}

# Choose model
Write-Host ""
Write-Host "🤖 Choose OpenAI model:" -ForegroundColor Green
Write-Host "   1. gpt-4o-mini (Recommended - Fast & Affordable)" -ForegroundColor Gray
Write-Host "   2. gpt-4o (More powerful, higher cost)" -ForegroundColor Gray
Write-Host "   3. gpt-3.5-turbo (Budget option)" -ForegroundColor Gray
Write-Host ""

$modelChoice = Read-Host "Enter choice (1-3, default: 1)"
$model = switch ($modelChoice) {
    "2" { "gpt-4o" }
    "3" { "gpt-3.5-turbo" }
    default { "gpt-4o-mini" }
}

# Create .env file
$envContent = @"
# Server Configuration
PORT=3001
NODE_ENV=development

# Database Configuration
DB_PATH=inventory.db

# CORS Configuration
CORS_ORIGIN=http://localhost:3000

# Logging Configuration
LOG_LEVEL=info

# OpenAI Configuration
OPENAI_API_KEY=$apiKey
OPENAI_MODEL=$model
OPENAI_ENABLED=true
"@

# Write to file
$envContent | Out-File -FilePath $envPath -Encoding UTF8

Write-Host ""
Write-Host "✅ Configuration saved to backend\.env" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Your settings:" -ForegroundColor Cyan
Write-Host "   Model: $model" -ForegroundColor Gray
Write-Host "   API Key: $($apiKey.Substring(0, 10))..." -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Green
Write-Host "   1. cd backend" -ForegroundColor Gray
Write-Host "   2. npm install" -ForegroundColor Gray
Write-Host "   3. npm run build" -ForegroundColor Gray
Write-Host "   4. npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 For more info, see GPT_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

