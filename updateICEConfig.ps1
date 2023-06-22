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
            $config.ice_Token="9898919b194bed5da79fc9542605c2ebcf6b07abb2c4c1179beff63b97e669bdc6be56e04008e9dbcfaa6e9282b74ac823a2fe5ee91dec1e1bc25e18b02f3951";
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
 