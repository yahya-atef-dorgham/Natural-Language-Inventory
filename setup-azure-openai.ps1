# Azure OpenAI Setup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Azure OpenAI Integration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

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

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
OPENAI_ENABLED=true
"@

$envPath = "backend_python\.env"

# Create .env file
$envContent | Out-File -FilePath $envPath -Encoding UTF8

Write-Host "Azure OpenAI configuration saved to backend_python\.env" -ForegroundColor Green
Write-Host ""
Write-Host "Your settings:" -ForegroundColor Cyan
Write-Host "   Endpoint: https://your-endpoint.openai.azure.com" -ForegroundColor Gray
Write-Host "   Deployment: gpt-4o" -ForegroundColor Gray
Write-Host "   API Version: 2025-01-01-preview" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "   1. cd backend_python" -ForegroundColor Gray
Write-Host "   2. python -m venv venv" -ForegroundColor Gray
Write-Host "   3. .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   4. pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   5. python src\main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
