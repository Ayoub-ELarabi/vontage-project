
import os
import datetime

BASE_URL = "https://vontage.app"

def generate_sitemap():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    today = datetime.date.today().isoformat()
    
    # Priority rules
    for file in files:
        priority = "0.8"
        if file == "index.html":
            priority = "1.0"
        elif file == "guides.html":
            priority = "0.9"
        elif file in ["contact.html", "privacy.html", "terms.html"]:
            priority = "0.5"
            
        url = f"{BASE_URL}/{file}"
        
        xml_content += "  <url>\n"
        xml_content += f"    <loc>{url}</loc>\n"
        xml_content += f"    <lastmod>{today}</lastmod>\n"
        xml_content += f"    <priority>{priority}</priority>\n"
        xml_content += "  </url>\n"
        
    xml_content += '</urlset>'
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated sitemap.xml with {len(files)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
