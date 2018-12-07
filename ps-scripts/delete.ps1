Write-Host "Calling local web service..."

$name = Read-Host 'Enter list name to delete'
$Url = "http://127.0.0.1:3000/list/" + $name
$response = Invoke-RestMethod -Method 'Delete' -Uri $Url -ContentType "application/json"
#Write-Host $response

$response | Format-Table -Property success
