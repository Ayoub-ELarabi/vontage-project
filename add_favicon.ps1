
$faviconLine = '    <link rel="icon" type="image/svg+xml" href="favicon.svg">'
$files = Get-ChildItem -Path . -Filter "*.html"

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    if ($content -notmatch "favicon.svg") {
        # Inject before stylesheet link or end of head
        if ($content -match '<link rel="stylesheet" href="styles.css">') {
            $content = $content.Replace('<link rel="stylesheet" href="styles.css">', "$faviconLine`n    <link rel="stylesheet" href=`"styles.css`">")
        } elseif ($content -match '</head>') {
            $content = $content.Replace('</head>', "$faviconLine`n</head>")
        }
        
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Host "Added favicon to $($file.Name)"
    }
}
