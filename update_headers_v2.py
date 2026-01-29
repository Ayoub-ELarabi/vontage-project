
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
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    filename = os.path.basename(filepath)
    modified = False

    # 1. Ensure FontAwesome
    if 'font-awesome' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'    {FONT_AWESOME_LINK}\n</head>')
            modified = True

    # 2. Update Header
    header_pattern = re.compile(r'<header.*?>.*?</header>', re.DOTALL)
    if header_pattern.search(content):
        content = header_pattern.sub(HEADER_HTML, content)
        modified = True

    # 3. Add Search Script
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
    root_dir = os.getcwd()
    excluded = ['index.html', 'guides.html', 'script.js', 'contact.html', 'update_headers.py', 'update_headers_v2.py']
    
    count = 0
    files = [f for f in os.listdir(root_dir) if f.endswith('.html') and f not in excluded]
    print(f"Found {len(files)} files to check.")
    
    for filename in files:
        if update_file(os.path.join(root_dir, filename)):
            print(f"Updated {filename}")
            count += 1
                
    print(f"Total files updated: {count}")

if __name__ == '__main__':
    main()
