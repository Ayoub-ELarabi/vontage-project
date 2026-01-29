
import os
import re

HEADER_HTML = """        <header class="global-header">
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
        </header>"""

SEARCH_SCRIPT = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('globalSearchInput');
            if (searchInput) {
                searchInput.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter') {
                        const query = e.target.value.trim();
                        if (query) {
                            window.location.href = `guides.html?q=${encodeURIComponent(query)}`;
                        }
                    }
                });
            }
        });
    </script>
"""

FONT_AWESOME_LINK = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    modified = False

    # 1. Ensure FontAwesome
    if 'font-awesome' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'    {FONT_AWESOME_LINK}\n</head>')
            modified = True

    # 2. Update Header
    # Pattern for articles
    header_pattern = re.compile(r'<header.*?>.*?</header>', re.DOTALL)
    
    if filename == 'contact.html':
        # Special case for contact.html
        # Remove old branding
        content = re.sub(r'<div class="branding">.*?</div>', '', content, flags=re.DOTALL)
        # Insert new header at start of app-container
        if '<div class="app-container">' in content:
            content = content.replace('<div class="app-container">', f'<div class="app-container" style="padding-top: 0; display: block;">\n{HEADER_HTML}')
            modified = True
    elif header_pattern.search(content):
        # Replace existing header
        content = header_pattern.sub(HEADER_HTML, content)
        modified = True
    elif '<div class="app-container"' in content:
        # If no header but app-container exists (and not index/guides which are excluded), maybe insert it?
        # Safe to assume check for body or app-container
        pass 

    # 3. Add Search Script
    # Check if script already exists (avoid duplicates if re-run)
    if 'globalSearchInput' not in content and filename != 'script.js':
         if '</body>' in content:
             content = content.replace('</body>', f'{SEARCH_SCRIPT}\n</body>')
             modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root_dir = r'c:\Users\lenovo\Desktop\vontage-project'
    excluded = ['index.html', 'guides.html', 'script.js']
    
    count = 0
    for filename in os.listdir(root_dir):
        if filename.endswith('.html') and filename not in excluded:
            if update_file(os.path.join(root_dir, filename)):
                print(f"Updated {filename}")
                count += 1
            else:
                print(f"Skipped {filename} (No changes needed or pattern mismatch)")
                
    print(f"Total files updated: {count}")

if __name__ == '__main__':
    main()
