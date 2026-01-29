
$c = Get-Content "seo-backlinks-bio-link-strategy.html" -Raw
Write-Host "Length: $($c.Length)"
if ($c -match '(?s)<header.*?>.*?</header>') {
    Write-Host "MATCHED!"
} else {
    Write-Host "NO MATCH"
    Write-Host "First 1000 chars:"
    Write-Host $c.Substring(0, 1000)
}
