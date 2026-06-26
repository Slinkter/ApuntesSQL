import re
import os

def markdown_to_html(md_content, title):
    # Split into lines
    lines = md_content.split('\n')
    html_body = []
    in_code_block = False
    code_lang = ""
    code_lines = []
    in_list = False
    in_quote = False
    quote_lines = []

    for line in lines:
        # Code Blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                in_code_block = False
                code_content = '\n'.join(code_lines)
                escaped_code = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                if code_lang == 'mermaid':
                    html_body.append(f'<div class="my-6 p-4 bg-emerald-950/20 border border-emerald-900/30 rounded-2xl overflow-hidden"><div class="mermaid text-center">{escaped_code}</div></div>')
                else:
                    html_body.append(f'<div class="my-6 relative"><div class="absolute right-4 top-3 text-xs text-stone-400 font-mono select-none">{code_lang.upper()}</div><pre class="bg-stone-900 text-stone-100 p-5 rounded-2xl overflow-x-auto border border-stone-800 font-mono text-sm leading-relaxed"><code>{escaped_code}</code></pre></div>')
                code_lines = []
            else:
                # Start of code block
                in_code_block = True
                code_lang = line.strip()[3:].strip()
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Blockquotes (Explanations)
        if line.strip().startswith('>'):
            if not in_quote:
                in_quote = True
            quote_lines.append(line.strip()[1:].strip())
            continue
        elif in_quote:
            in_quote = False
            quote_text = ' '.join(quote_lines)
            # Parse bold/italic inside blockquote
            quote_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', quote_text)
            quote_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', quote_text)
            quote_text = re.sub(r'`(.*?)`', r'<code class="px-1.5 py-0.5 bg-stone-200/60 dark:bg-stone-800/60 rounded text-rose-600 dark:text-rose-400 font-mono text-xs">\1</code>', quote_text)
            # Check if it starts with "La analogía" or similar
            if "analogía" in quote_text.lower():
                html_body.append(f'<div class="my-6 p-5 bg-amber-500/10 border-l-4 border-amber-500 rounded-r-2xl"><div class="text-xs font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 mb-1">💡 Analogía Didáctica</div><p class="text-stone-700 dark:text-stone-300 italic text-sm leading-relaxed">{quote_text}</p></div>')
            else:
                html_body.append(f'<div class="my-6 p-5 bg-stone-100 dark:bg-stone-900 border-l-4 border-stone-400 rounded-r-2xl"><p class="text-stone-700 dark:text-stone-300 italic text-sm leading-relaxed">{quote_text}</p></div>')
            quote_lines = []

        # Lists
        if line.strip().startswith('* ') or line.strip().startswith('- '):
            if not in_list:
                in_list = True
                html_body.append('<ul class="list-disc pl-6 my-4 space-y-2 text-stone-600 dark:text-stone-300 leading-relaxed text-sm">')
            list_content = line.strip()[2:]
            # Format inline styles
            list_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', list_content)
            list_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', list_content)
            list_content = re.sub(r'`(.*?)`', r'<code class="px-1.5 py-0.5 bg-stone-200/60 dark:bg-stone-800/60 rounded text-rose-600 dark:text-rose-400 font-mono text-xs">\1</code>', list_content)
            list_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="text-emerald-700 dark:text-emerald-400 hover:underline font-semibold">\1</a>', list_content)
            html_body.append(f'<li>{list_content}</li>')
            continue
        elif in_list:
            in_list = False
            html_body.append('</ul>')

        # Headings
        if line.strip().startswith('### '):
            heading_text = line.strip()[4:]
            html_body.append(f'<h4 class="text-md font-bold text-stone-800 dark:text-stone-200 mt-6 mb-3 flex items-center gap-2 border-b border-stone-200/60 dark:border-stone-800/60 pb-1">{heading_text}</h4>')
            continue
        elif line.strip().startswith('## '):
            heading_text = line.strip()[3:]
            html_body.append(f'<h3 class="text-lg font-bold text-emerald-900 dark:text-emerald-300 mt-8 mb-4 border-l-4 border-emerald-600 pl-3">{heading_text}</h3>')
            continue
        elif line.strip().startswith('# '):
            heading_text = line.strip()[2:]
            html_body.append(f'<h2 class="text-2xl font-black tracking-tight text-stone-900 dark:text-stone-100 mb-6">{heading_text}</h2>')
            continue

        # Normal paragraphs or blank lines
        if line.strip() == '':
            continue

        # Inline formatting
        p_text = line.strip()
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
        p_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_text)
        p_text = re.sub(r'`(.*?)`', r'<code class="px-1.5 py-0.5 bg-stone-200/60 dark:bg-stone-800/60 rounded text-rose-600 dark:text-rose-400 font-mono text-xs">\1</code>', p_text)
        p_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="text-emerald-700 dark:text-emerald-400 hover:underline font-semibold">\1</a>', p_text)

        html_body.append(f'<p class="text-stone-700 dark:text-stone-300 text-sm leading-relaxed my-3">{p_text}</p>')

    if in_list:
        html_body.append('</ul>')

    body_content = '\n'.join(html_body)

    # Full HTML layout with Organic Style & Tailwind v4
    template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'forest' }});
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #fbf9f4; /* Alabaster Cream */
            color: #2c3530; /* Forest Slate */
        }}
        pre, code {{
            font-family: 'JetBrains Mono', monospace;
        }}
    </style>
</head>
<body class="min-h-screen dark:bg-stone-950 dark:text-stone-100 transition-colors duration-300">
    <div class="max-w-4xl mx-auto px-4 py-12">
        <header class="mb-10 text-center">
            <h1 class="text-3xl font-extrabold tracking-tight text-emerald-950 dark:text-emerald-300 mb-2">{title}</h1>
            <p class="text-stone-600 dark:text-stone-400 text-sm">Libro de Trabajo de Ejercicios de Base de Datos Enriquecido</p>
        </header>

        <main class="bg-white dark:bg-stone-900 border border-stone-200/80 dark:border-stone-800/80 rounded-3xl p-8 shadow-xl shadow-emerald-950/5">
            <article class="prose dark:prose-invert max-w-none">
                {body_content}
            </article>
        </main>

        <footer class="mt-12 text-center text-xs text-stone-500 dark:text-stone-600">
            <p>© 2026 PostgreSQL Academy | Academia de Arquitectura de Datos</p>
        </footer>
    </div>
</body>
</html>
"""
    return template

# Convert the files
files_to_convert = [
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/0.prerrequisitos.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/0.prerrequisitos.html", "0. Prerrequisitos y Configuración de AWS EC2"),
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/1.basico.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/1.basico.html", "1. Ejercicios SQL Nivel Básico"),
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/2.intermedio.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/2.intermedio.html", "2. Ejercicios SQL Nivel Intermedio"),
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/3.avanzado.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/Lab01/Ejercicios/3.avanzado.html", "3. Ejercicios SQL Nivel Avanzado"),
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/1.basico.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/1.basico.html", "SQL Básico y Mecánica de Motor"),
    ("C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/2.intermedio.md", "C:/Users/LJCR/Documents/GitHub/ApuntesSQL/Lab/2.intermedio.html", "SQL Intermedio, Agrupaciones y Joins")
]

for src, dest, title in files_to_convert:
    if os.path.exists(src):
        print(f"Leyendo: {src}")
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_out = markdown_to_html(content, title)
        
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(html_out)
        print(f"Escrito con éxito: {dest}")
    else:
        print(f"No existe el archivo de origen: {src}")
