import os
import re

dir_path = "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes"

for i in range(2, 17):
    filename = f"semana_{i:02d}.html"
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        continue
    
    print(f"Procesando: {filename}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Fix header
    header_pattern = re.compile(
        r'(<header class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 shadow-sm">\s*)'
        r'(<h1 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">.*?</h1>\s*)'
        r'(<p class="mt-2 text-sm font-medium text-slate-500 dark:text-slate-400">.*?</p>\s*)'
        r'(</header>)',
        re.DOTALL
    )
    
    def replace_header(match):
        start, h1, p, end = match.groups()
        if "max-w-7xl" not in h1 and "max-w-7xl" not in start:
            # Clean up entities inside title or details if any
            h1_clean = h1.strip()
            p_clean = p.strip()
            return f'{start}    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">\n        {h1_clean}\n        {p_clean}\n    </div>\n{end}'
        return match.group(0)
        
    content = header_pattern.sub(replace_header, content)
    
    # 2. Fix PALABRAS CLAVE block
    keywords_pattern = re.compile(
        r'(<h3 class="text-xs font-bold tracking-wider text-slate-400 dark:text-slate-500 uppercase mb-4">\s*PALABRAS CLAVE\s*</h3>\s*<ul class="space-y-4">)(.*?)(</ul>)',
        re.DOTALL
    )
    
    def replace_keywords(match):
        header_ul, items_content, closing_ul = match.groups()
        
        # Match <li class="text-sm"><strong>§ TERM</strong>DESC</li>
        item_regex = re.compile(r'<li class="text-sm"><strong>(§.*?)</strong>(.*?)</li>', re.DOTALL)
        
        new_items = []
        for item_match in item_regex.finditer(items_content):
            term, desc = item_match.groups()
            new_item = (
                f'                <li class="text-sm">\n'
                f'                    <strong class="text-indigo-600 dark:text-indigo-400 block mb-0.5">{term.strip()}</strong>\n'
                f'                    <span class="text-slate-600 dark:text-slate-400">{desc.strip()}</span>\n'
                f'                </li>'
            )
            new_items.append(new_item)
            
        if new_items:
            formatted_items = "\n".join(new_items)
            return (
                f'<div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm hover:shadow-md transition-shadow">\n'
                f'            <h3 class="text-xs font-bold tracking-wider text-slate-400 dark:text-slate-500 uppercase mb-4">Palabras Clave</h3>\n'
                f'            <ul class="space-y-4">\n'
                f'{formatted_items}\n'
                f'            </ul>\n'
                f'        </div>'
            )
        return match.group(0)
        
    content = keywords_pattern.sub(replace_keywords, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Refactorizado con éxito: {filename}")
