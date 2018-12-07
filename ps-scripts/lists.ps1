Write-Host "Calling local web service..."

$Url = "http://127.0.0.1:3000/list"
$response = Invoke-RestMethod -Method 'Get' -Uri $url -ContentType "application/json"
#Write-Host $response


$lists = $response.data
$lists | Format-Table -Property Name, Store


