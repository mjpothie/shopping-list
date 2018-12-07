Write-Host "Calling local web service..."

$name = Read-Host 'Enter list name'
$Url = "http://127.0.0.1:3000/list/" + $name
$response = Invoke-RestMethod -Method 'Get' -Uri $Url -ContentType "application/json"
#Write-Host $response

$data = $response.data
$data | Format-Table -Property Name,Store