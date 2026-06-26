import re
import os

def parse_mermaid_to_html(mermaid_content):
    lines = [line.strip() for line in mermaid_content.split('\n') if line.strip()]
    if not lines:
        return ""
    
    diagram_type = lines[0].lower()
    
    # 1. FLOWCHARTS
    if 'flowchart' in diagram_type or 'graph' in diagram_type:
        nodes = {}
        connections = []
        
        # Regex to match nodes: A[Label], B(Label), C{Label}, A[(Label)], etc.
        node_regex = re.compile(r'([a-zA-Z0-9_-]+)(?:\["?(.*?)"?\]|\("?(.*?)"?\)|\{"?(.*?)"?\}|\(\("?(.*?)"?\)\))')
        # Regex to match connections: A --> B or A -->|Label| B
        conn_regex = re.compile(r'([a-zA-Z0-9_-]+)\s*-->\s*(?:\|(.*?)\|)?\s*([a-zA-Z0-9_-]+)')
        
        for line in lines[1:]:
            # Parse connections first
            conn_match = conn_regex.search(line)
            if conn_match:
                source, label, target = conn_match.groups()
                connections.append({
                    'source': source,
                    'target': target,
                    'label': label if label else ""
                })
            
            # Parse nodes to collect custom labels
            for match in node_regex.finditer(line):
                node_id = match.group(1)
                # Find the first non-empty group for the label
                label = next((g for g in match.groups()[1:] if g), node_id)
                nodes[node_id] = label.replace(r'\n', ' ').strip()
        
        # Build a sequential flow representation in HTML
        html = ['<div class="pure-html-flowchart">']
        
        # Determine execution order (simple linear / branching layout helper)
        seen_targets = {c['target'] for c in connections}
        roots = [n for n in nodes if n not in seen_targets]
        
        if not roots and nodes:
            roots = [list(nodes.keys())[0]]
            
        def render_node(node_id, visited=None):
            if visited is None:
                visited = set()
            if node_id in visited:
                lbl = nodes.get(node_id, node_id)
                return f'<div class="flow-node flow-node-step opacity-50 font-mono text-xs">↺ {lbl}</div>'
            
            # Add to visited
            visited.add(node_id)
            
            label = nodes.get(node_id, node_id)
            # Check if this node is a decision block
            is_decision = '{' in label or '?' in label or 'WHERE' in label or 'Filter' in label or 'Eval' in label
            node_class = "flow-node-decision" if is_decision else "flow-node-step"
            
            node_html = f'<div class="flow-node {node_class}">{label}</div>'
            
            # Find outgoing connections
            outgoings = [c for c in connections if c['source'] == node_id]
            if outgoings:
                # If branching (decision)
                if len(outgoings) > 1:
                    branch_html = ['<div class="flow-branches-wrapper">']
                    for conn in outgoings:
                        branch_label = f'<span class="branch-label">{conn["label"]}</span>' if conn['label'] else ''
                        branch_html.append(f'<div class="flow-branch"><div class="flow-arrow-vertical">↓ {branch_label}</div>{render_node(conn["target"], visited.copy())}</div>')
                    branch_html.append('</div>')
                    return node_html + '\n'.join(branch_html)
                else:
                    conn = outgoings[0]
                    arrow_label = f'<span class="arrow-label">{conn["label"]}</span>' if conn['label'] else ''
                    return f'{node_html}<div class="flow-arrow-vertical">↓ {arrow_label}</div>{render_node(conn["target"], visited)}'
            return node_html

        for root in roots:
            html.append(render_node(root))
            
        html.append('</div>')
        return '\n'.join(html)

    # 2. SEQUENCE DIAGRAMS
    elif 'sequencediagram' in diagram_type:
        participants = []
        steps = []
        
        part_regex = re.compile(r'participant\s+(.*)')
        msg_regex = re.compile(r'([a-zA-Z0-9_ -]+)\s*->>\s*([a-zA-Z0-9_ -]+):\s*(.*)')
        note_regex = re.compile(r'Note\s+over\s+(.*):\s*(.*)')
        
        for line in lines[1:]:
            part_match = part_regex.match(line)
            if part_match:
                participants.append(part_match.group(1).strip())
                continue
                
            msg_match = msg_regex.match(line)
            if msg_match:
                source, target, msg = msg_match.groups()
                steps.append({
                    'type': 'message',
                    'source': source.strip(),
                    'target': target.strip(),
                    'content': msg.strip()
                })
                continue
                
            note_match = note_regex.match(line)
            if note_match:
                over, note_text = note_match.groups()
                steps.append({
                    'type': 'note',
                    'over': over.strip(),
                    'content': note_text.strip()
                })
                
        # Fallback if participants not explicitly declared
        if not participants:
            seen_parts = set()
            for s in steps:
                if s['type'] == 'message':
                    seen_parts.add(s['source'])
                    seen_parts.add(s['target'])
            participants = list(seen_parts)

        # Render sequence as a clean timelines chat block
        html = ['<div class="pure-html-sequence">']
        for step in steps:
            if step['type'] == 'message':
                html.append(f'<div class="seq-step"><div class="seq-actors"><span class="actor-source">{step["source"]}</span> ➔ <span class="actor-target">{step["target"]}</span></div><div class="seq-message">{step["content"]}</div></div>')
            elif step['type'] == 'note':
                html.append(f'<div class="seq-note"><span class="seq-note-title">Nota:</span> {step["content"]}</div>')
        html.append('</div>')
        return '\n'.join(html)
        
    return f'<pre class="raw-diagram"><code>{mermaid_content}</code></pre>'


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
                in_code_block = False
                code_content = '\n'.join(code_lines)
                if code_lang == 'mermaid':
                    html_flow = parse_mermaid_to_html(code_content)
                    html_body.append(html_flow)
                else:
                    escaped_code = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html_body.append(f'<div class="code-block-wrapper"><div class="code-lang-badge">{code_lang.upper()}</div><pre><code>{escaped_code}</code></pre></div>')
                code_lines = []
            else:
                in_code_block = True
                code_lang = line.strip()[3:].strip()
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Escape raw text to prevent mathematical expressions like < or > from breaking HTML
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Blockquotes (Explanations)
        if escaped_line.strip().startswith('&gt;'):
            if not in_quote:
                in_quote = True
            quote_lines.append(escaped_line.strip()[4:].strip())
            continue
        elif in_quote:
            in_quote = False
            quote_text = ' '.join(quote_lines)
            quote_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', quote_text)
            quote_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', quote_text)
            quote_text = re.sub(r'`(.*?)`', r'<code>\1</code>', quote_text)
            if "analogía" in quote_text.lower() or "analoga" in quote_text.lower():
                html_body.append(f'<div class="callout-box callout-analogy"><div class="callout-title">💡 Analogía Didáctica</div><p>{quote_text}</p></div>')
            else:
                html_body.append(f'<div class="callout-box callout-note"><p>{quote_text}</p></div>')
            quote_lines = []

        # Lists
        if escaped_line.strip().startswith('* ') or escaped_line.strip().startswith('- '):
            if not in_list:
                in_list = True
                html_body.append('<ul class="list-style-disc">')
            list_content = escaped_line.strip()[2:]
            list_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', list_content)
            list_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', list_content)
            list_content = re.sub(r'`(.*?)`', r'<code>\1</code>', list_content)
            list_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', list_content)
            html_body.append(f'<li>{list_content}</li>')
            continue
        elif in_list:
            in_list = False
            html_body.append('</ul>')

        # Headings
        if escaped_line.strip().startswith('### '):
            heading_text = escaped_line.strip()[4:]
            html_body.append(f'<h4>{heading_text}</h4>')
            continue
        elif escaped_line.strip().startswith('## '):
            heading_text = escaped_line.strip()[3:]
            html_body.append(f'<h3>{heading_text}</h3>')
            continue
        elif escaped_line.strip().startswith('# '):
            heading_text = escaped_line.strip()[2:]
            html_body.append(f'<h2>{heading_text}</h2>')
            continue

        if escaped_line.strip() == '':
            continue

        # Normal paragraphs formatting
        p_text = escaped_line.strip()
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
        p_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_text)
        p_text = re.sub(r'`(.*?)`', r'<code>\1</code>', p_text)
        p_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', p_text)

        html_body.append(f'<p>{p_text}</p>')

    if in_list:
        html_body.append('</ul>')

    body_content = '\n'.join(html_body)

    # Full HTML layout with native CSS variables for Light/Dark mode and perfect Mobile-First design
    template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }} else {{
            document.documentElement.classList.remove('dark');
        }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #ffffff;       /* Pure Crisp White */
            --bg-card: #ffffff;
            --text-main: #111111;     /* High Contrast Black */
            --text-muted: #666666;
            --primary: #000000;
            --accent: #ff3333;        /* Swiss Red */
            --border: #111111;        /* Sharp 1px Borders */
            --code-bg: #f5f5f5;
            --code-text: #ff3333;
            --shadow: none;
            --radius-md: 0px;         /* Sharp Corners */
            --radius-lg: 0px;
        }}

        :root.dark {{
            --bg-main: #0a0a0a;   /* Deep Ashen Black */
            --bg-card: #121212;
            --text-main: #f0f0f0;
            --text-muted: #888888;
            --primary: #ffffff;
            --accent: #ff5555;    /* Swiss Bright Red */
            --border: #333333;
            --code-bg: #181818;
            --code-text: #ff5555;
            --shadow: none;
        }}

        /* Swiss Minimalist Theme Switcher Button */
        .theme-toggle-btn {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 100;
            padding: 0.35rem 0.75rem;
            border: 1px solid var(--border);
            background-color: var(--bg-card);
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
        }}
        .theme-toggle-btn:hover {{
            background-color: var(--primary);
            color: var(--bg-main);
        }}

        /* Reset and Base Styles */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Sitka Small', 'Sitka Text', 'Sitka Subheading', 'Lora', 'Georgia', 'Times New Roman', serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
            padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(1rem, env(safe-area-inset-bottom)) max(1rem, env(safe-area-inset-left));
        }}

        /* Mobile-First Layout container */
        .wrapper {{
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 1rem 0.5rem;
        }}

        @media (min-width: 640px) {{
            .wrapper {{
                padding: 2rem 1.5rem;
            }}
        }}

        /* Header block */
        header {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
        }}

        header h1 {{
            font-family: 'Sitka Display', 'Sitka Subheading', 'Lora', 'Georgia', serif;
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.25;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
        }}

        @media (min-width: 640px) {{
            header h1 {{
                font-size: 2.25rem;
            }}
        }}

        header p {{
            font-size: 0.875rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* Main card content */
        main {{
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            box-shadow: var(--shadow);
        }}

        @media (min-width: 640px) {{
            main {{
                padding: 2.5rem;
            }}
        }}

        /* Typography spacing inside article */
        article p {{
            margin-bottom: 1.25rem;
            font-size: 0.95rem;
            color: var(--text-main);
        }}

        article h2 {{
            font-family: 'Sitka Display', 'Sitka Subheading', 'Lora', 'Georgia', serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--primary);
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}

        article h3 {{
            font-family: 'Sitka Subheading', 'Lora', 'Georgia', serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--primary);
            margin-top: 1.75rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid var(--accent);
            padding-left: 0.75rem;
        }}

        article h4 {{
            font-family: 'Sitka Text', 'Lora', 'Georgia', serif;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
        }}

        /* Inline formatting */
        strong {{
            font-weight: 700;
            color: var(--primary);
        }}

        a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s ease;
        }}

        a:hover {{
            color: var(--text-main);
            text-decoration: underline;
        }}

        /* Inline code */
        code {{
            font-family: 'JetBrains Mono', monospace;
            background-color: var(--code-bg);
            color: var(--code-text);
            padding: 0.15rem 0.35rem;
            border-radius: 6px;
            font-size: 0.85em;
        }}

        /* Lists */
        .list-style-disc {{
            list-style-type: disc;
            padding-left: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .list-style-disc li {{
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }}

        /* Code block layouts */
        .code-block-wrapper {{
            position: relative;
            margin: 1.5rem 0;
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .code-lang-badge {{
            position: absolute;
            right: 1rem;
            top: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            color: #8c8c8c;
            user-select: none;
        }}

        pre {{
            font-family: 'JetBrains Mono', monospace;
            background-color: #0d120f; /* Dark background for code in both modes */
            color: #e2e8f0;
            padding: 1.25rem;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            font-size: 0.85rem;
            line-height: 1.6;
        }}

        pre code {{
            background-color: transparent !important;
            color: inherit !important;
            padding: 0 !important;
            font-size: inherit !important;
        }}

        /* Pure HTML Flowchart styling (Replacing Mermaid) */
        .pure-html-flowchart {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 2rem 0;
            padding: 1.5rem 1rem;
            border: 1px solid var(--border);
            background-color: var(--code-bg);
        }}

        .flow-node {{
            padding: 0.75rem 1.25rem;
            font-size: 0.875rem;
            font-weight: 700;
            text-align: center;
            border: 1px solid var(--border);
            background-color: var(--bg-card);
            color: var(--text-main);
            min-width: 200px;
            max-width: 100%;
        }}

        .flow-node-step {{
            border-left: 4px solid var(--primary);
        }}

        .flow-node-decision {{
            border-left: 4px solid var(--accent);
            background-color: rgba(255, 51, 51, 0.04);
        }}

        .flow-arrow-vertical {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--accent);
            margin: 0.5rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            font-weight: 700;
        }}
        
        .arrow-label {{
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 0.1rem;
        }}

        .flow-branches-wrapper {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            width: 100%;
            margin-top: 0.5rem;
            flex-wrap: wrap;
        }}

        .flow-branch {{
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            min-width: 180px;
        }}

        .branch-label {{
            font-size: 0.7rem;
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            padding: 0.1rem 0.4rem;
            margin-top: 0.1rem;
            font-weight: 700;
        }}

        /* Pure HTML Sequence Diagram styling */
        .pure-html-sequence {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 2rem 0;
            padding: 1.5rem;
            border: 1px solid var(--border);
            background-color: var(--code-bg);
        }}

        .seq-step {{
            border-left: 2px solid var(--accent);
            padding-left: 1rem;
        }}

        .seq-actors {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 0.25rem;
        }}

        .seq-message {{
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .seq-note {{
            font-size: 0.85rem;
            font-style: italic;
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            padding: 0.5rem 1rem;
            color: var(--text-muted);
        }}
        
        .seq-note-title {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent);
        }}

        /* Callout Boxes */
        .callout-box {{
            padding: 1.25rem;
            border-radius: var(--radius-md);
            margin: 1.5rem 0;
            border-left: 4px solid;
            font-size: 0.9rem;
        }}

        .callout-box p {{
            margin-bottom: 0;
            font-size: inherit;
        }}

        .callout-note {{
            background-color: var(--code-bg);
            border-color: var(--text-muted);
            color: var(--text-main);
        }}

        .callout-analogy {{
            background-color: rgba(255, 51, 51, 0.04);
            border-color: var(--accent);
            color: var(--text-main);
        }}

        .callout-title {{
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 0.25rem;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Footer */
        footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>
    <button id="theme-toggle" class="theme-toggle-btn">[ MODO: OSCURO ]</button>
    <div class="wrapper">
        <header>
            <h1>{title}</h1>
            <p>Libro de Trabajo de Ejercicios de Base de Datos Enriquecido</p>
        </header>

        <main>
            <article>
                {body_content}
            </article>
        </main>

        <footer>
            <p>© 2026 PostgreSQL Academy | Academia de Arquitectura de Datos</p>
        </footer>
    </div>

    <script>
        const themeToggleBtn = document.getElementById('theme-toggle');
        
        function updateToggleText() {{
            if (document.documentElement.classList.contains('dark')) {{
                themeToggleBtn.textContent = '[ MODO: CLARO ]';
            }} else {{
                themeToggleBtn.textContent = '[ MODO: OSCURO ]';
            }}
        }}
        
        updateToggleText();

        themeToggleBtn.addEventListener('click', () => {{
            if (document.documentElement.classList.contains('dark')) {{
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }} else {{
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }}
            updateToggleText();
        }});
    </script>
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
