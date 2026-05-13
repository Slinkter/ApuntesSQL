import os
import re
import markdown

files = [
    ('01_Fundamentos/Clase_1.02_Teoria_Relacional.md', 'semana_02.html'),
    ('01_Fundamentos/Clase_1.03_Tipologia_BD.md', 'semana_03.html'),
    ('01_Fundamentos/Clase_1.04_SDLC_Migrations.md', 'semana_04.html')
]

base_dir = r'C:\Users\LJCR\Documents\GitHub\ApuntesSQL\Apuntes'

for md_file, html_file in files:
    md_path = os.path.join(base_dir, md_file)
    html_path = os.path.join(base_dir, html_file)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    html_from_md = markdown.markdown(md_content)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    injection = f'<section class="architect-insight">\n<h4>💡 Insight del Arquitecto</h4>\n{html_from_md}\n</section>\n'
    
    # Try to find <div class="box box-note">...</div>
    # Using regex to find the end of the box-note div
    pattern = re.compile(r'(<div class="box box-note">.*?</div>\s*)', re.DOTALL)
    match = pattern.search(html_content)
    
    if match:
        new_html = html_content[:match.end()] + injection + html_content[match.end():]
    else:
        # If not found, insert at the beginning of <div class="main-content">
        pattern2 = re.compile(r'(<div class="main-content">\s*)')
        match2 = pattern2.search(html_content)
        if match2:
            new_html = html_content[:match2.end()] + injection + html_content[match2.end():]
        else:
            print(f'Failed to find injection point in {html_file}')
            continue
            
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f'Successfully injected {md_file} into {html_file}')
