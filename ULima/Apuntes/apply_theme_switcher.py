import os
import re

directory = "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes"

# The toggle button styles to inject in the style tag
style_to_inject = """
        @custom-variant dark (&:where(.dark, .dark *));
        .theme-toggle-btn {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 100;
            padding: 0.35rem 0.75rem;
            border: 1px solid #111111;
            background-color: #ffffff;
            color: #111111;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
        }
        html.dark .theme-toggle-btn {
            border-color: #333333;
            background-color: #121212;
            color: #f0f0f0;
        }
        .theme-toggle-btn:hover {
            background-color: #111111;
            color: #ffffff;
        }
        html.dark .theme-toggle-btn:hover {
            background-color: #ffffff;
            color: #111111;
        }
"""

# The pre-head script to inject to prevent flash
head_script = """
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    </script>
"""

# The toggle button and body script
body_button = '<button id="theme-toggle" class="theme-toggle-btn">[ MODO: OSCURO ]</button>'

body_script = """
    <script>
        const themeToggleBtn = document.getElementById('theme-toggle');
        
        function updateToggleText() {
            if (document.documentElement.classList.contains('dark')) {
                themeToggleBtn.textContent = '[ MODO: CLARO ]';
            } else {
                themeToggleBtn.textContent = '[ MODO: OSCURO ]';
            }
        }
        
        updateToggleText();

        themeToggleBtn.addEventListener('click', () => {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
            updateToggleText();
        });
    </script>
</body>
"""

# Process all files matching semana_*.html and index.html
files = [f for f in os.listdir(directory) if f.startswith("semana_") and f.endswith(".html")] + ["index.html"]

for filename in files:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        print(f"Modificando: {filename}")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Inject script in <head>
        if "<script>" not in content or "color-theme" not in content:
            content = content.replace("<head>", f"<head>\n{head_script}")

        # 2. Inject style rules in <style>
        if '<style type="text/tailwindcss">' in content:
            content = content.replace('<style type="text/tailwindcss">', f'<style type="text/tailwindcss">\n{style_to_inject}')
        elif '<style>' in content:
            content = content.replace('<style>', f'<style>\n{style_to_inject}')
        else:
            # If no style tag exists (like in index.html), create one
            style_block = f"<style>{style_to_inject}</style>"
            content = content.replace("</head>", f"{style_block}\n</head>")

        # 3. Inject button after body tag
        # Use regex to replace <body> with <body> + button
        if 'id="theme-toggle"' not in content:
            content = re.sub(r'(<body[^>]*>)', f'\\1\n    {body_button}', content)

        # 4. Inject script before </body>
        if "themeToggleBtn" not in content:
            content = content.replace("</body>", body_script)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Guardado exitoso: {filename}")
