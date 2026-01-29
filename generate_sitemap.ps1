
$baseUrl = "https://vontage.app"
$files = Get-ChildItem -Path . -Filter "*.html"
$today = (Get-Date).ToString("yyyy-MM-dd")

$xml = '<?xml version="1.0" encoding="UTF-8"?>' + "`n"
$xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"

foreach ($file in $files) {
    $priority = "0.8"
    if ($file.Name -eq "index.html") { $priority = "1.0" }
    elseif ($file.Name -eq "guides.html") { $priority = "0.9" }
    elseif ($file.Name -in "contact.html", "privacy.html", "terms.html") { $priority = "0.5" }

    $url = "$baseUrl/$($file.Name)"

    $xml += "  <url>`n"
    $xml += "    <loc>$url</loc>`n"
    $xml += "    <lastmod>$today</lastmod>`n"
    $xml += "    <priority>$priority</priority>`n"
    $xml += "  </url>`n"
}

$xml += '</urlset>'

$xml | Set-Content -Path "sitemap.xml" -Encoding UTF8
Write-Host "Generated sitemap.xml with $($files.Count) URLs."
