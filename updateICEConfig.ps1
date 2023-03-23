param(
     $avofolder, $exename
)

try
{
 Write-Output ("Updating avo config file") 
 
    $efile = Split-Path -Path $exename -Leaf 
    $efile =$efile.ToLower()

    if ($efile.StartsWith('avoassureclient')) 
    { 
        if ($efile.Contains(" ")) {$efile = $efile.Split(" ")[0] + ".exe"; }
        $config=Get-Content $avofolder/AvoAssure/assets/Config.json -raw | ConvertFrom-Json
        $wurl = $efile.Replace(".exe", "");

#--for non-trial license
        if ($efile.StartsWith('avoassureclient0')) 
        {
            $wurl = $wurl.Replace("avoassureclient0_","");
            $config.isTrial=0;

        }
#--for trial license
        if ($efile.StartsWith('avoassureclient1')) 
        {
            $config.isTrial=1;
            $wurl = $wurl.Replace("avoassureclient1_","");
        }
    
        $config.server_ip = $wurl ;
        Copy-Item $avofolder/AvoAssure/assets/Config.json -Destination $avofolder/AvoAssure/assets/Config.bak
        $config | ConvertTo-Json | set-content $avofolder/AvoAssure/assets/Config.json
    }
    else {
           Write-Output ("No changes made");
    }
   Write-Output ("success") 
    
   # Read-Host
    
} 
catch 
{
    Write-Output "Error in updating configuring url"
}
 