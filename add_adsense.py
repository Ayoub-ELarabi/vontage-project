import os

# The AdSense code to inject
adsense_code = """    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7439455242484505"
     crossorigin="anonymous"></script>
"""

def inject_code():
    count = 0
    # Walk through current directory
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if already injected to avoid duplicates
                if "client=ca-pub-7439455242484505" in content:
                    print(f"Skipping {file} (already has AdSense code)")
                    continue
                
                # Inject before </head>
                if "</head>" in content:
                    new_content = content.replace("</head>", f"{adsense_code}</head>")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    print(f"Injected into {file}")
                    count += 1
                else:
                    print(f"Warning: No </head> tag in {file}")

    print(f"Complete! Injected AdSense code into {count} files.")

if __name__ == "__main__":
    inject_code()
