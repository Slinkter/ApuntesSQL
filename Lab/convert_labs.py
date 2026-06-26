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

    # 3. ER DIAGRAMS
    elif 'erdiagram' in diagram_type:
        relationships = []
        entities = {}
        current_entity = None
        
        for line in lines[1:]:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Check if this is the start of an entity block
            if '{' in line_str:
                entity_name = line_str.split('{')[0].strip()
                current_entity = entity_name
                entities[current_entity] = []
                continue
            
            # Check if this is the end of an entity block
            if '}' in line_str:
                current_entity = None
                continue
            
            # If we are inside an entity block, parse attributes
            if current_entity:
                attr_parts = line_str.split()
                if len(attr_parts) >= 2:
                    attr_type = attr_parts[0]
                    attr_name = attr_parts[1]
                    attr_key = " ".join(attr_parts[2:]) if len(attr_parts) > 2 else ""
                    entities[current_entity].append({
                        'type': attr_type,
                        'name': attr_name,
                        'key': attr_key
                    })
                continue
            
            # Otherwise, check for relationship
            if ':' in line_str:
                parts = line_str.split(':')
                rel_part = parts[0].strip()
                label = parts[1].replace('"', '').strip()
                
                rel_match = re.match(r'([a-zA-Z0-9_-]+)\s+([|o{}~-]+)\s+([a-zA-Z0-9_-]+)', rel_part)
                if rel_match:
                    ent1, op, ent2 = rel_match.groups()
                    relationships.append({
                        'ent1': ent1,
                        'op': op,
                        'ent2': ent2,
                        'label': label
                    })
        
        # Build pure HTML/CSS ER diagram
        html = ['<div class="pure-html-er-diagram">']
        
        # 1. Relationships list
        if relationships:
            html.append('<div class="er-relationships">')
            html.append('<h4>Relaciones de la Base de Datos</h4>')
            html.append('<ul class="er-relations-list">')
            for rel in relationships:
                op_desc = "Relación"
                if "o{" in rel['op'] or "}o" in rel['op']:
                    op_desc = "Uno a Varios (1:N)"
                elif "||" in rel['op'] and "||" in rel['op']:
                    op_desc = "Uno a Uno (1:1)"
                
                html.append(f'<li><span class="entity-badge">{rel["ent1"]}</span> ➔ <span class="relation-label">"{rel["label"]}" ({op_desc})</span> ➔ <span class="entity-badge">{rel["ent2"]}</span></li>')
            html.append('</ul></div>')
            
        # 2. Entity details grid
        if entities:
            html.append('<div class="er-entities-grid">')
            for ent_name, attrs in entities.items():
                html.append(f'<div class="er-entity-card">')
                html.append(f'<div class="er-entity-header">{ent_name}</div>')
                html.append('<table class="er-entity-table">')
                for attr in attrs:
                    key_badge = ""
                    if "PK" in attr['key']:
                        key_badge = '<span class="key-badge pk">PK</span>'
                    elif "FK" in attr['key']:
                        key_badge = '<span class="key-badge fk">FK</span>'
                    
                    html.append(f'<tr><td class="attr-name">{attr["name"]} {key_badge}</td><td class="attr-type">{attr["type"]}</td></tr>')
                html.append('</table></div>')
            html.append('</div>')
            
        html.append('</div>')
        return '\n'.join(html)
        
    return f'<pre class="raw-diagram"><code>{mermaid_content}</code></pre>'


def render_table_to_html(table_rows):
    html_table = ['<div class="table-wrapper"><table>']
    has_thead = False
    for row in table_rows:
        row_html = []
        if row['is_header']:
            html_table.append('<thead><tr>')
            for cell in row['cells']:
                formatted_cell = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                formatted_cell = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_cell)
                formatted_cell = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted_cell)
                formatted_cell = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', formatted_cell)
                row_html.append(f'<th>{formatted_cell}</th>')
            html_table.append(''.join(row_html))
            html_table.append('</tr></thead><tbody>')
            has_thead = True
        else:
            html_table.append('<tr>')
            for cell in row['cells']:
                formatted_cell = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                formatted_cell = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_cell)
                formatted_cell = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted_cell)
                formatted_cell = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', formatted_cell)
                row_html.append(f'<td>{formatted_cell}</td>')
            html_table.append(''.join(row_html))
            html_table.append('</tr>')
    if has_thead:
        html_table.append('</tbody>')
    html_table.append('</table></div>')
    return '\n'.join(html_table)

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
    in_table = False
    table_rows = []

    def close_open_structures():
        nonlocal in_list, in_quote, in_table, table_rows, quote_lines
        res = []
        if in_table:
            in_table = False
            res.append(render_table_to_html(table_rows))
            table_rows = []
        if in_list:
            in_list = False
            res.append('</ul>')
        if in_quote:
            in_quote = False
            quote_text = ' '.join(quote_lines)
            quote_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', quote_text)
            quote_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', quote_text)
            quote_text = re.sub(r'`(.*?)`', r'<code>\1</code>', quote_text)
            if "analogía" in quote_text.lower() or "analoga" in quote_text.lower():
                res.append(f'<div class="callout-box callout-analogy"><div class="callout-title">💡 Analogía Didáctica</div><p>{quote_text}</p></div>')
            else:
                res.append(f'<div class="callout-box callout-note"><p>{quote_text}</p></div>')
            quote_lines = []
        return res

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
                html_body.extend(close_open_structures())
                in_code_block = True
                code_lang = line.strip()[3:].strip()
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Escape raw text to prevent mathematical expressions like < or > from breaking HTML
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Table rows check
        is_table_row = escaped_line.strip().startswith('|') and escaped_line.strip().endswith('|')
        if is_table_row:
            if in_list or in_quote:
                if in_list:
                    in_list = False
                    html_body.append('</ul>')
                if in_quote:
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

            if not in_table:
                in_table = True
                table_rows = []

            raw_cells = [cell.strip() for cell in escaped_line.strip().split('|')[1:-1]]
            is_separator = all(re.match(r'^:?-+:?$', cell) for cell in raw_cells) and len(raw_cells) > 0
            if is_separator:
                if table_rows:
                    table_rows[-1]['is_header'] = True
            else:
                table_rows.append({
                    'is_header': False,
                    'cells': raw_cells
                })
            continue

        # Blockquotes (Explanations)
        if escaped_line.strip().startswith('&gt;'):
            if in_list or in_table:
                if in_list:
                    in_list = False
                    html_body.append('</ul>')
                if in_table:
                    in_table = False
                    html_body.append(render_table_to_html(table_rows))
                    table_rows = []
            if not in_quote:
                in_quote = True
            quote_lines.append(escaped_line.strip()[4:].strip())
            continue

        # Lists
        if escaped_line.strip().startswith('* ') or escaped_line.strip().startswith('- '):
            if in_quote or in_table:
                if in_quote:
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
                if in_table:
                    in_table = False
                    html_body.append(render_table_to_html(table_rows))
                    table_rows = []
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

        # For any other line, close list, table, or quote if they were active
        closed_tags = close_open_structures()
        if closed_tags:
            html_body.extend(closed_tags)

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

    # End of loop, close anything left open
    html_body.extend(close_open_structures())

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
    <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    <style type="text/tailwindcss">
        @theme {{
            --color-bg-main: #ffffff;       /* Pure Crisp White */
            --color-bg-card: #ffffff;
            --color-text-main: #111111;     /* High Contrast Black */
            --color-text-muted: #666666;
            --color-primary: #000000;
            --color-accent: #ff3333;        /* Swiss Red */
            --color-border: #111111;        /* Sharp 1px Borders */
            --color-code-bg: #f5f5f5;
            --color-code-text: #ff3333;
            
            --font-sitka: 'Sitka Small', 'Sitka Text', 'Sitka Subheading', 'Lora', 'Georgia', serif;
        }}

        @custom-variant dark (&:where(.dark, .dark *));

        .dark {{
            --color-bg-main: #0a0a0a;   /* Deep Ashen Black */
            --color-bg-card: #121212;
            --color-text-main: #f0f0f0;
            --color-text-muted: #888888;
            --color-primary: #ffffff;
            --color-accent: #ff5555;    /* Swiss Bright Red */
            --color-border: #333333;
            --color-code-bg: #181818;
            --color-code-text: #ff5555;
        }}

        /* Swiss Minimalist Theme Switcher Button */
        .theme-toggle-btn {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 100;
            padding: 0.35rem 0.75rem;
            border: 1px solid var(--color-border);
            background-color: var(--color-bg-card);
            color: var(--color-text-main);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
        }}
        .theme-toggle-btn:hover {{
            background-color: var(--color-primary);
            color: var(--color-bg-main);
        }}

        /* Reset and Base Styles */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-sitka);
            background-color: var(--color-bg-main);
            color: var(--color-text-main);
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
            color: var(--color-primary);
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
            color: var(--color-text-muted);
            font-weight: 500;
        }}

        /* Main card content */
        main {{
            background-color: var(--color-bg-card);
            border: 1px solid var(--color-border);
            border-radius: 0px;
            padding: 1.25rem;
            box-shadow: none;
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
            color: var(--color-text-main);
        }}

        article h2 {{
            font-family: 'Sitka Display', 'Sitka Subheading', 'Lora', 'Georgia', serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--color-primary);
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--color-border);
            padding-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}

        article h3 {{
            font-family: 'Sitka Subheading', 'Lora', 'Georgia', serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--color-primary);
            margin-top: 1.75rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid var(--color-accent);
            padding-left: 0.75rem;
        }}

        article h4 {{
            font-family: 'Sitka Text', 'Lora', 'Georgia', serif;
            font-size: 1rem;
            font-weight: 700;
            color: var(--color-text-main);
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
        }}

        /* Inline formatting */
        strong {{
            font-weight: 700;
            color: var(--color-primary);
        }}

        a {{
            color: var(--color-accent);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s ease;
        }}

        a:hover {{
            color: var(--color-text-main);
            text-decoration: underline;
        }}

        /* Inline code */
        code {{
            font-family: 'JetBrains Mono', monospace;
            background-color: var(--color-code-bg);
            color: var(--color-code-text);
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

        /* Tables styling */
        .table-wrapper {{
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin: 1.5rem 0;
            border: 1px solid var(--color-border);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            text-align: left;
        }}

        th, td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--color-border);
        }}

        th {{
            background-color: var(--color-code-bg);
            color: var(--color-primary);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Code block layouts */
        .code-block-wrapper {{
            position: relative;
            margin: 1.5rem 0;
            border-radius: 0px;
            overflow: hidden;
            border: 1px solid var(--color-border);
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

        /* Pure HTML ER Diagram styling */
        .pure-html-er-diagram {{
            margin: 2rem 0;
            padding: 1.5rem;
            border: 1px solid var(--color-border);
            background-color: var(--color-code-bg);
        }}

        .er-relationships {{
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--color-border);
            padding-bottom: 1rem;
        }}

        .er-relations-list {{
            list-style-type: none !important;
            padding-left: 0 !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }}

        .er-relations-list li {{
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .entity-badge {{
            background-color: var(--color-primary);
            color: var(--color-bg-main);
            padding: 0.15rem 0.5rem;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.7rem;
            border: 1px solid var(--color-border);
        }}

        .relation-label {{
            color: var(--color-text-muted);
            font-weight: 600;
        }}

        .er-entities-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}

        .er-entity-card {{
            background-color: var(--color-bg-card);
            border: 1px solid var(--color-border);
        }}

        .er-entity-header {{
            background-color: var(--color-primary);
            color: var(--color-bg-main);
            padding: 0.4rem 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            border-bottom: 1px solid var(--color-border);
        }}

        .er-entity-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
        }}

        .er-entity-table td {{
            padding: 0.35rem 0.65rem;
            border-bottom: 1px solid var(--color-border);
        }}

        .er-entity-table tr:last-child td {{
            border-bottom: none;
        }}

        .attr-name {{
            font-weight: 600;
            color: var(--color-text-main);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.25rem;
        }}

        .attr-type {{
            color: var(--color-text-muted);
            text-align: right;
        }}

        .key-badge {{
            font-size: 0.6rem;
            font-weight: 700;
            padding: 0.05rem 0.25rem;
            color: #ffffff;
        }}

        .key-badge.pk {{
            background-color: var(--color-accent);
        }}

        .key-badge.fk {{
            background-color: #666666;
        }}

        /* Pure HTML Flowchart styling (Replacing Mermaid) */
        .pure-html-flowchart {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 2rem 0;
            padding: 1.5rem 1rem;
            border: 1px solid var(--color-border);
            background-color: var(--color-code-bg);
        }}

        .flow-node {{
            padding: 0.75rem 1.25rem;
            font-size: 0.875rem;
            font-weight: 700;
            text-align: center;
            border: 1px solid var(--color-border);
            background-color: var(--color-bg-card);
            color: var(--color-text-main);
            min-width: 200px;
            max-width: 100%;
        }}

        .flow-node-step {{
            border-left: 4px solid var(--color-primary);
        }}

        .flow-node-decision {{
            border-left: 4px solid var(--color-accent);
            background-color: rgba(255, 51, 51, 0.04);
        }}

        .flow-arrow-vertical {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--color-accent);
            margin: 0.5rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            font-weight: 700;
        }}
        
        .arrow-label {{
            font-size: 0.7rem;
            color: var(--color-text-muted);
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
            background-color: var(--color-bg-card);
            border: 1px solid var(--color-border);
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
            border: 1px solid var(--color-border);
            background-color: var(--color-code-bg);
        }}

        .seq-step {{
            border-left: 2px solid var(--color-accent);
            padding-left: 1rem;
        }}

        .seq-actors {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--color-text-muted);
            margin-bottom: 0.25rem;
        }}

        .seq-message {{
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .seq-note {{
            font-size: 0.85rem;
            font-style: italic;
            background-color: var(--color-bg-card);
            border: 1px solid var(--color-border);
            padding: 0.5rem 1rem;
            color: var(--color-text-muted);
        }}
        
        .seq-note-title {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--color-accent);
        }}

        /* Callout Boxes */
        .callout-box {{
            padding: 1.25rem;
            border-radius: 0px;
            margin: 1.5rem 0;
            border-left: 4px solid;
            font-size: 0.9rem;
        }}

        .callout-box p {{
            margin-bottom: 0;
            font-size: inherit;
        }}

        .callout-note {{
            background-color: var(--color-code-bg);
            border-color: var(--color-text-muted);
            color: var(--color-text-main);
        }}

        .callout-analogy {{
            background-color: rgba(255, 51, 51, 0.04);
            border-color: var(--color-accent);
            color: var(--color-text-main);
        }}

        .callout-title {{
            font-weight: 700;
            color: var(--color-accent);
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
            color: var(--color-text-muted);
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
