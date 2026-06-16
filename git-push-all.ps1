param(
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "== Git: preparando envio para o GitHub ==" -ForegroundColor Cyan

if (-not (Test-Path ".git")) {
    Write-Host "Erro: execute este script na raiz de um repositorio Git." -ForegroundColor Red
    exit 1
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = Read-Host "Digite a mensagem do commit"
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    Write-Host "Erro: mensagem de commit vazia." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Status atual:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "Adicionando arquivos..." -ForegroundColor Cyan
git add .

$statusAfterAdd = git status --short

if ([string]::IsNullOrWhiteSpace(($statusAfterAdd | Out-String))) {
    Write-Host "Nada para commitar. O repositorio ja esta atualizado localmente." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Criando commit: $Message" -ForegroundColor Cyan
    git commit -m "$Message"
}

$branch = git branch --show-current

if ([string]::IsNullOrWhiteSpace($branch)) {
    Write-Host "Erro: nao foi possivel identificar a branch atual." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Enviando para origin/$branch..." -ForegroundColor Cyan
git push -u origin $branch

Write-Host ""
Write-Host "Concluido. Alteracoes enviadas para o GitHub." -ForegroundColor Green
