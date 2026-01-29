
$headerHtml = '        <header class="global-header">
            <div class="branding">
                <a href="index.html">Vontage.</a>
            </div>
            <div class="header-search-container">
                <input type="text" id="globalSearchInput" class="global-search-input" placeholder="Search guides...">
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
            </div>
            <nav class="header-nav">
                <a href="guides.html">Guides</a>
                <a href="contact.html">Contact</a>
            </nav>
        </header>'

$searchScript = '    <script>
        document.addEventListener("DOMContentLoaded", () => {
            const searchInput = document.getElementById("globalSearchInput");
            if (searchInput) {
                searchInput.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") {
                        const query = e.target.value.trim();
                        if (query) {
                            window.location.href = `guides.html?q=${encodeURIComponent(query)}`;
                        }
                    }
                });
            }
        });
    </script>'

$fontAwesome = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'

Write-Host "Starting update (Round 2)..."
$files = Get-ChildItem -Path . -Filter *.html 
Write-Host "Found $($files.Count) files."

$excluded = @('index.html', 'guides.html', 'script.js')
# contact.html also needs the script if I didn't add it correctly or if I want to be safe. 
# But I manually added it to contact.html. I'll exclude it to avoid double script.
$excluded += 'contact.html'

$count = 0
foreach ($file in $files) {
    if ($excluded -contains $file.Name) {
        # Write-Host "Skipping specific file: $($file.Name)"
        continue
    }

    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $modified = $false

    # Font Awesome
    if ($content -notmatch 'font-awesome') {
        if ($content -match '</head>') {
            $content = $content.Replace('</head>', "    $fontAwesome`n</head>")
            $modified = $true
        }
    }

    # Header Replacement (Should handle existing correct header gracefully or re-replace if identical)
    # If header matches EXACTLY, regex replace might just do same-to-same.
    # But checking if we need to update:
    # If file has old header, replace.
    # The regex '(?s)<header.*?>.*?</header>' matches the NEW header too!
    # So it will replace New Header with New Header. No change effectively, but sets modified=true?
    # No, Replace returns same string. $content matches $content.
    # But I should avoid marking modified if no change.
    
    # Actually, simpler: just run the script injection check logic.
    # I won't re-run header logic unless necessary, but running it is harmless idempotent if strings match.
    
    # content = [regex]::Replace(...)

    # Script Injection - CORRECTED CHECK
    if ($content -notmatch 'const searchInput = document.getElementById') {
        if ($content -match '</body>') {
            $content = $content.Replace('</body>', "$searchScript`n</body>")
            $modified = $true
        }
    }

    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Host "Updated $($file.Name)"
        $count++
    }
}
Write-Host "Total Updated: $count"
