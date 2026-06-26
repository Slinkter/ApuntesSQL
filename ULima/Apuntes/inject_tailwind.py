import os
import glob
import re

os.chdir(r'C:\Users\LJCR\Documents\GitHub\ApuntesSQL\ULima\Apuntes')

tailwind_script = '<script src="https://unpkg.com/@tailwindcss/browser@4"></script>\n</head>'

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'tailwindcss/browser' not in content:
        new_content = content.replace('</head>', tailwind_script)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Injected Tailwind into {file}')
