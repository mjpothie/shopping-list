Write-Host "Calling local web service..."

$Url = "http://127.0.0.1:3000/list"
$listname = Read-Host 'Enter list name'
$storename = Read-Host 'Enter store name'
$Body = @{
    listName = $listname
	storeName = $storename
	
} | convertto-json
$response = Invoke-RestMethod -Method 'Post' -Uri $Url -Body $Body -ContentType "application/json"
#Write-Host $response

$response | Format-Table -Property success

