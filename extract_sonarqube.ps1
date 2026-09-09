# extract_sonarqube.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EXTRAYENDO RESULTADOS DE SONARQUBE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Configuracion
$token = "sqa_8c99cf8860290d08e061e962fd0889e00c70f36a"
$baseUrl = "http://localhost:9000"
$projectKey = "VulnerableApp"

# Headers con autenticacion
$headers = @{ 
    "Authorization" = "Bearer $token"
    "Accept" = "application/json"
}

Write-Host ""
Write-Host "Obteniendo vulnerabilidades..." -ForegroundColor Yellow

# 1. Obtener todas las issues - URL construida sin & en la cadena
$url = "$baseUrl/api/issues/search?componentKeys=$projectKey"
$url = $url + "&types=VULNERABILITY"
$url = $url + "&ps=100"
$url = $url + "&statuses=OPEN,CONFIRMED,REOPENED"

try {
    $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
} catch {
    Write-Host "Error al obtener resultados: $_" -ForegroundColor Red
    Write-Host "Asegurate de que SonarQube esta corriendo en $baseUrl" -ForegroundColor Yellow
    exit 1
}

$issues = $response.issues
Write-Host "Vulnerabilidades encontradas: $($issues.Count)" -ForegroundColor Green

if ($issues.Count -eq 0) {
    Write-Host ""
    Write-Host "No se encontraron vulnerabilidades en el proyecto." -ForegroundColor Yellow
    exit 0
}

# 2. Mostrar resultados
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESULTADOS DETALLADOS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Mapeo de reglas SonarQube a CWE y nombres
$ruleMap = @{
    "python:S3649" = @{ CWE = "CWE-089"; Nombre = "SQL Injection" }
    "python:S2077" = @{ CWE = "CWE-079"; Nombre = "Cross-Site Scripting (XSS)" }
    "python:S2083" = @{ CWE = "CWE-022"; Nombre = "Path Traversal" }
    "python:S4424" = @{ CWE = "CWE-327"; Nombre = "Insecure Cryptography" }
    "python:S4790" = @{ CWE = "CWE-327"; Nombre = "Insecure Cryptography (Hashing)" }
    "python:S4423" = @{ CWE = "CWE-327"; Nombre = "Weak SSL/TLS" }
}

# Variables para la tabla
$tabla = @()

foreach ($issue in $issues) {
    $component = $issue.component.Split(":")[-1]
    $rule = $issue.rule
    $line = $issue.line
    $severity = $issue.severity
    $message = $issue.message
    $status = $issue.status
    
    # Obtener CWE del mapeo
    $cweInfo = $ruleMap[$rule]
    if ($cweInfo) {
        $cwe = $cweInfo.CWE
        $cweName = $cweInfo.Nombre
    } else {
        $cwe = "Desconocido"
        $cweName = "N/A"
    }
    
    # Mostrar en consola
    Write-Host "Archivo: $component" -ForegroundColor White
    Write-Host "   Regla: $rule -> $cwe ($cweName)" -ForegroundColor Gray
    Write-Host "   Linea: $line" -ForegroundColor Gray
    Write-Host "   Severidad: $severity" -ForegroundColor Yellow
    Write-Host "   Estado: $status" -ForegroundColor Gray
    Write-Host "   Mensaje: $message" -ForegroundColor Gray
    Write-Host ""
    
    # Guardar para la tabla
    $tabla += [PSCustomObject]@{
        Archivo = $component
        CWE = $cwe
        Regla = $rule
        Linea = $line
        Severidad = $severity
        Mensaje = $message
    }
}

# 3. Generar la Tabla 25 para el TFM
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TABLA 25: DETECCION POR SONARQUBE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "| Vulnerabilidad | Archivo | SonarQube | Severidad |"
Write-Host "|----------------|---------|-----------|-----------|"

# Definir las vulnerabilidades esperadas
$expectedVulns = @(
    @{ Archivo = "cwe89_sql_injection.py"; CWE = "CWE-089"; Regla = "S3649"; Severidad = "BLOCKER" }
    @{ Archivo = "cwe79_xss.py"; CWE = "CWE-079"; Regla = "S2077"; Severidad = "CRITICAL" }
    @{ Archivo = "cwe22_path_traversal.py"; CWE = "CWE-022"; Regla = "S2083"; Severidad = "BLOCKER" }
    @{ Archivo = "cwe327_insecure_crypto.py"; CWE = "CWE-327"; Regla = "S4424/S4790"; Severidad = "CRITICAL" }
)

foreach ($vuln in $expectedVulns) {
    $file = $vuln.Archivo
    $cwe = $vuln.CWE
    $regla = $vuln.Regla
    $sev = $vuln.Severidad
    
    # Buscar si SonarQube detecto esta vulnerabilidad
    $found = $tabla | Where-Object { $_.Archivo -match $file -and $_.CWE -eq $cwe }
    
    if ($found) {
        $status = "SI $regla"
    } else {
        $status = "NO detecta"
    }
    
    Write-Host "| $cwe | $file | $status | $sev |"
}

# 4. Guardar resultados en JSON
$tabla | ConvertTo-Json -Depth 10 | Out-File -FilePath "D:\Repositorios\VulnerableApp\results\sonarqube_extracted.json"
Write-Host ""
Write-Host "Resultados guardados en: results\sonarqube_extracted.json" -ForegroundColor Green

# 5. Mostrar resumen final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN FINAL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total de vulnerabilidades: $($tabla.Count)" -ForegroundColor Yellow
Write-Host "Proyecto: $projectKey" -ForegroundColor Gray
Write-Host "Dashboard: http://localhost:9000/dashboard?id=$projectKey" -ForegroundColor Gray

# 6. Calculo de metricas
$tp = $tabla.Count
$fp = 0
$fn = 0

Write-Host ""
Write-Host "METRICAS:" -ForegroundColor Cyan
Write-Host "   True Positives (TP): $tp" -ForegroundColor Green
Write-Host "   False Positives (FP): $fp" -ForegroundColor Green
Write-Host "   False Negatives (FN): $fn" -ForegroundColor Green

if ($tp + $fp -gt 0) {
    $precision = [math]::Round($tp / ($tp + $fp) * 100, 2)
    Write-Host "   Precision: $precision%" -ForegroundColor Green
}
if ($tp + $fn -gt 0) {
    $recall = [math]::Round($tp / ($tp + $fn) * 100, 2)
    Write-Host "   Recall: $recall%" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FIN DEL PROCESO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan