$url = "https://www.autohotkey.com/download/1.1/AutoHotkey_1.1.31.01_setup.exe"
$output = ".\ci\ahk_install.exe"

$wc = New-Object System.Net.WebClient
$UserAgent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"
$wc.Headers.Add([System.Net.HttpRequestHeader]::UserAgent, $UserAgent);
$wc.DownloadFile($url, $output)

.\ci\ahk_install.exe /S
