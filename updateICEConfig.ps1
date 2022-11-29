param(
     $avofolder, $exename
)

try
{
 Write-Output ($avofolder)


 #Read-Host
 
    $efile = Split-Path -Path $exename -Leaf
    
    $efile =$efile.ToLower()

    if ($efile -clike 'avoassureclient*') { 
        
		if ($efile.Contains(" ")) {$efile = $efile.Split(" ")[0] + ".exe"; }
		 

        $wurl = $efile.Replace(".exe", ".avoassure.ai");
      # Write-Output ("1" + $wurl)



        $wurl = $wurl.Replace("avoassureclient_","");
        $newsvr = '"server_ip": "'+ $wurl + '",' 
        (Get-Content $avofolder/AvoAssure/assets/Config.json) -replace '"server_ip": "localhost",' ,$newsvr  | Out-File -FilePath $avofolder/AvoAssure/assets/Config.json -Force -encoding default
       # Write-Output ("2" + $wurl)
    }
    else {
           Write-Output ("No changes made");
    }
    
   # Read-Host
    
} 
catch 
{
    Write-Output "Error in updating configuring url"
}
 