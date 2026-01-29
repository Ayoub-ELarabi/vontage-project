
$NewHeader = @"
    <header class="global-header" style="width: 100%; padding: 1rem 2rem; background: rgba(0,0,0,0.2);">
        <div class="header-inner">
            <!-- Left: Branding -->
            <div class="branding">
                <a href="index.html">Vontage.</a>
            </div>

            <!-- Center: Search -->
            <div class="header-search-container">
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input type="text" id="globalSearchInput" class="global-search-input" placeholder="Search guides...">
            </div>

            <!-- Right: Nav -->
            <nav class="header-nav">
                <a href="guides.html">Guides</a>
                <a href="contact.html">Contact</a>
            </nav>
        </div>
    </header>
"@

$NewFooter = @"
    <footer class="app-footer">
        <p>&copy; 2026 Vontage. All rights reserved.</p>
        <div class="footer-links">
            <a href="guides.html">Guides</a>
            <a href="privacy.html">Privacy Policy</a>
            <a href="terms.html">Terms of Service</a>
            <a href="contact.html">Contact</a>
        </div>
    </footer>
    <script src="script.js"></script>
"@

$files = Get-ChildItem -Path . -Filter "*.html"

foreach ($file in $files) {
    if ($file.Name -eq "index.html") {
        continue
    }

    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    # Regex update for HEADER
    # Matches <header ... > ... </header> including newlines
    $content = $content -replace '(?s)<header.*?</header>', ""
    # Inject new header after <body>
    if ($content -match '<body>') {
        $content = $content -replace '<body>', "<body>`r`n$NewHeader"
    }

    # Regex update for FOOTER
    $content = $content -replace '(?s)<footer.*?</footer>', ""
    # Inject new footer before </body>
    if ($content -match '</body>') {
        $content = $content -replace '</body>', "$NewFooter`r`n</body>"
    }
    
    # Fix main app-container top padding if needed (remove style="" inline override)
    # This is a bit risky to regex globally, but we can look for specific patterns from old templates.
    # For now, let's stick to Header/Footer replacement as that solves the layout issues.

    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    Write-Host "Updated $($file.Name)"
}
