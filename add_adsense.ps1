$adsenseCode = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7439455242484505" crossorigin="anonymous"></script>'

$files = Get-ChildItem -Path . -Filter *.html -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    if ($content -notmatch "client=ca-pub-7439455242484505") {
        if ($content -match "</head>") {
            $newContent = $content -replace "</head>", "$adsenseCode`n</head>"
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            Write-Host "Injected AdSense into $($file.Name)"
        } else {
            Write-Warning "No </head> tag found in $($file.Name)"
        }
    } else {
        Write-Host "Skipping $($file.Name) - already verified."
    }
}
Write-Host "Done!"
