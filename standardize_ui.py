
import os
import re

# Template for the new standardized header
NEW_HEADER = """
    <header class="global-header" style="width: 100%; padding: 1rem 2rem; background: rgba(0,0,0,0.2);">
        <div class="header-inner">
            <!-- Left: Nav -->
            <nav class="header-nav">
                <a href="guides.html">Guides</a>
                <a href="contact.html">Contact</a>
            </nav>

            <!-- Center: Search -->
            <div class="header-search-container">
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input type="text" id="globalSearchInput" class="global-search-input" placeholder="Search guides...">
            </div>

            <!-- Right: Branding -->
            <div class="branding">
                <a href="index.html">Vontage.</a>
            </div>
        </div>
    </header>
"""

# Template for the standardized footer
NEW_FOOTER = """
    <footer class="app-footer">
        <p>&copy; 2026 Vontage. All rights reserved.</p>
        <div class="footer-links">
            <a href="guides.html">Guides</a>
            <a href="privacy.html">Privacy Policy</a>
            <a href="terms.html">Terms of Service</a>
            <a href="contact.html">Contact</a>
        </div>
    </footer>
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip index.html since we are updating it manually
    if filepath.endswith('index.html'):
        return

    # 1. Remove old Header and Insert New Header
    # Strategy: Find <body> tag. If header exists inside body, remove it. Insert new header after <body>.
    
    # Remove existing header blocks
    content = re.sub(r'<header.*?</header>', '', content, flags=re.DOTALL)
    
    # Insert new header after <body> opening tag
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + NEW_HEADER, 1)
    
    # 2. Remove old Footer and Insert New Footer
    # Remove existing footer blocks
    content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)
    
    # Insert new footer before </body> closing tag
    if '</body>' in content:
        content = content.replace('</body>', NEW_FOOTER + '\n</body>', 1)
        
    # 3. Fix Main Container (Remove app-container wrapping if it causes issues, or ensure padding)
    # Ideally, we just ensure the header/footer are OUTSIDE the main container.
    # The regex replacement above naturally places them at top/bottom of body.
    # So we just need to ensure the remaining content is valid.
    
    # Optional: Basic cleanup of double newlines
    # content = re.sub(r'\n\s*\n', '\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

def main():
    directory = "."
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            process_file(os.path.join(directory, filename))

if __name__ == "__main__":
    main()
