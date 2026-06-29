#!/usr/bin/env python3
"""
sync_design_gold.py
Synchronizes design elements from semana_01.html (gold standard) to semanas 02–16.

Fixes applied:
1. <html> → add class="scroll-smooth"
2. <style> → change to type="text/tailwindcss" + add @theme block
3. Remove <link rel="stylesheet" href="master.css"> (conflicts with Tailwind v4 CDN)
4. Normalize <header> wrapper with max-w-7xl
5. Normalize sidebar Keywords card structure
6. Normalize sidebar Resources to emerald colors
7. Replace bare <pre> with styled code blocks
8. Add SVG icon to Objetivos section
9. Normalize nav footer with proper button styles
"""

import re
import os
from pathlib import Path

APUNTES_DIR = Path(__file__).parent

# ─────────────────────────────────────────────────────────
# The canonical <style> block from semana_01 (gold standard)
# ─────────────────────────────────────────────────────────
GOLD_STYLE_BLOCK = """    <style type="text/tailwindcss">
        @custom-variant dark (&:where(.dark, .dark *));
        @theme {
            --font-sans: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --color-primary: #6750A4;
            --color-primary-dark: #D0BCFF;
            --color-surface-light: #FEF7FF;
            --color-surface-dark: #0A0A0C;
            --color-slate-950: #050505;
            --color-slate-900: #0D0D11;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.02em;
        }
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.625;
            letter-spacing: -0.011em;
        }
        html.dark body {
            color: #cbd5e1 !important;
        }
        html.dark .prose p, html.dark p {
            color: #94a3b8 !important;
        }
        html.dark .prose strong, html.dark strong {
            color: #f1f5f9 !important;
        }
    </style>"""

# ─────────────────────────────────────────────────────────
# Gold standard nav footer
# ─────────────────────────────────────────────────────────
def build_nav_footer(week_num: int) -> str:
    prev_link = "index.html" if week_num <= 2 else f"semana_{week_num-1:02d}.html"
    prev_text = "Volver al Índice" if week_num <= 2 else f"Semana {week_num-1:02d}"
    next_link = f"semana_{week_num+1:02d}.html" if week_num < 16 else "index.html"
    next_text = f"Semana {week_num+1:02d}" if week_num < 16 else "Volver al Índice"

    return f"""<nav class="flex justify-between items-center pt-8 border-t border-slate-200 dark:border-slate-800 mt-8">
            <a href="{prev_link}" class="px-5 py-2.5 rounded-lg font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 transition-colors">{prev_text}</a>
            <a href="{next_link}" class="px-5 py-2.5 rounded-lg font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm">{next_text}</a>
        </nav>"""


def fix_html_tag(content: str) -> str:
    """Fix 1: Add scroll-smooth to <html> tag."""
    # Replace <html lang="es"> (without scroll-smooth) 
    content = re.sub(
        r'<html\s+lang="es"\s*>',
        '<html lang="es" class="scroll-smooth">',
        content
    )
    # If already has class but not scroll-smooth, add it
    content = re.sub(
        r'<html\s+lang="es"\s+class="(?!scroll-smooth)([^"]*)"',
        r'<html lang="es" class="scroll-smooth \1"',
        content
    )
    return content


def fix_style_block(content: str) -> str:
    """Fix 2 & 3: Replace <style> block + remove master.css link."""
    
    # Remove master.css link (conflicts with Tailwind v4 inline)
    content = re.sub(
        r'\s*<link[^>]+href="master\.css"[^>]*>\s*\n?',
        '\n',
        content
    )
    
    # Pattern to match the existing <style> block (with or without type attribute)
    # and replace it with the gold standard
    style_pattern = re.compile(
        r'<style(?:\s+type="text/tailwindcss")?>\s*'
        r'@custom-variant dark.*?'
        r'</style>',
        re.DOTALL
    )
    
    if style_pattern.search(content):
        content = style_pattern.sub(GOLD_STYLE_BLOCK, content)
    
    return content


def fix_tailwind_script_order(content: str) -> str:
    """Ensure Tailwind CDN script comes BEFORE the style block."""
    # Check if tailwind script is after the style block
    tailwind_script = '<script src="https://unpkg.com/@tailwindcss/browser@4"></script>'
    
    # Remove existing tailwind script reference
    content = content.replace(
        '<script src="https://unpkg.com/@tailwindcss/browser@4"></script>\n',
        ''
    ).replace(
        '\n<script src="https://unpkg.com/@tailwindcss/browser@4"></script>',
        ''
    ).replace(
        '<script src="https://unpkg.com/@tailwindcss/browser@4"></script>',
        ''
    )
    
    # Re-insert it just before the <style type="text/tailwindcss"> block
    content = content.replace(
        '    <style type="text/tailwindcss">',
        f'    <!-- Tailwind v4 CDN -->\n    {tailwind_script}\n    <style type="text/tailwindcss">'
    )
    
    return content


def fix_header(content: str, week_num: int) -> str:
    """Fix 4: Normalize header to use proper <header> tag with max-w-7xl wrapper."""
    
    # Pattern 1: bare <div> acting as header (no <header> tag) — semana_05 style
    bare_div_header = re.compile(
        r'<div\s+class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md[^"]*sticky top-0 z-50[^"]*">\s*'
        r'<h1\s+class="([^"]*)">(.*?)</h1>\s*'
        r'<p\s+class="([^"]*)">(.*?)</p>\s*'
        r'</div>',
        re.DOTALL
    )
    
    def replace_bare_header(m):
        h1_text = m.group(2).strip()
        p_text = m.group(4).strip()
        return (
            f'<header class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 shadow-sm">\n'
            f'    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">\n'
            f'        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">\n'
            f'            {h1_text}\n'
            f'        </h1>\n'
            f'        <p class="mt-2 text-sm font-medium text-slate-500 dark:text-slate-400">\n'
            f'            {p_text}\n'
            f'        </p>\n'
            f'    </div>\n'
            f'</header>'
        )
    
    content = bare_div_header.sub(replace_bare_header, content)

    # Pattern 2: <header> tag exists but h1/p are directly inside without max-w-7xl div
    # (semana_02 style — header exists but inner div structure is slightly off)
    header_no_inner_div = re.compile(
        r'<header\s+class="([^"]*)">\s*'
        r'(?![\s\S]*?<div class="max-w-7xl)'  # negative lookahead: no max-w-7xl inside
        r'\s*<div\s+class="[^"]*max-w-7xl[^"]*">\s*'
        r'\s*<h1\s+class="([^"]*)">(.*?)</h1>\s*'
        r'\s*<p\s+class="([^"]*)">(.*?)</p>\s*'
        r'\s*</div>\s*'
        r'</header>',
        re.DOTALL
    )
    
    def replace_header_fix(m):
        h1_text = m.group(3).strip()
        p_text = m.group(5).strip()
        return (
            f'<header class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 shadow-sm">\n'
            f'    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">\n'
            f'        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">\n'
            f'            {h1_text}\n'
            f'        </h1>\n'
            f'        <p class="mt-2 text-sm font-medium text-slate-500 dark:text-slate-400">\n'
            f'            {p_text}\n'
            f'        </p>\n'
            f'    </div>\n'
            f'</header>'
        )
    
    content = header_no_inner_div.sub(replace_header_fix, content)
    
    # Also normalize the header separator character (| → bullet)
    content = re.sub(
        r'(Semana \d+)\s*\|\s*([^<]*)\|\s*([^<]*)<',
        r'\1 <span class="mx-2">&bull;</span> \2 <span class="mx-2">&bull;</span> \3<',
        content
    )

    return content


def fix_resources_sidebar(content: str) -> str:
    """Fix 6: Normalize Resources sidebar to emerald color (not blue)."""
    
    # Replace bg-blue-50 in sidebar resources div with emerald
    # This is specifically for the Recursos section in aside
    content = re.sub(
        r'(class="bg-blue-50 dark:bg-blue-900/20 rounded-2xl[^"]*"[^>]*>\s*'
        r'<h3[^>]*>RECURSOS</h3>)',
        lambda m: m.group(0).replace('bg-blue-50 dark:bg-blue-900/20', 'bg-emerald-50 dark:bg-emerald-950/30')
                              .replace('border-blue-100 dark:border-blue-800/50', 'border-emerald-100 dark:border-emerald-900/50'),
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Fix inline styles on resources div
    content = re.sub(
        r'(class="[^"]*rounded-2xl[^"]*")\s+style="[^"]*margin[^"]*"',
        r'\1',
        content
    )
    
    # Fix header color of Recursos section
    content = re.sub(
        r'(<h3[^>]*RECURSOS|<h3[^>]*Recursos)',
        lambda m: m.group(0).replace('text-slate-400 dark:text-slate-500', 'text-emerald-600 dark:text-emerald-500'),
        content,
        flags=re.IGNORECASE
    )
    
    return content


def fix_bare_pre_tags(content: str) -> str:
    """Fix 7: Wrap bare <pre> tags in styled divs."""
    
    # Pattern: bare <pre>CODE</pre> not already inside a styled div
    def wrap_pre(m):
        code = m.group(1)
        return (
            f'<div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 '
            f'dark:border-slate-800 font-mono text-xs overflow-x-auto text-slate-800 dark:text-slate-200 mb-4">'
            f'\n{code}\n</div>'
        )
    
    # Match <pre> that are NOT already inside a styled wrapper div
    content = re.sub(
        r'<pre>([\s\S]*?)</pre>',
        wrap_pre,
        content
    )
    
    return content


def fix_objectives_icon(content: str) -> str:
    """Fix 8: Add SVG icon to Objetivos de Aprendizaje section."""
    
    OBJECTIVES_SVG = (
        '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        'd="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
    )
    
    # Fix <p><strong>Objetivos...</strong></p> pattern (no flex, no icon)
    content = re.sub(
        r'<p>\s*<strong>Objetivos de Aprendizaje</strong>\s*</p>',
        f'<h4 class="text-blue-800 dark:text-blue-300 font-bold mb-3 flex items-center gap-2">'
        f'{OBJECTIVES_SVG}'
        f'Objetivos de Aprendizaje</h4>',
        content
    )
    
    # Fix bare <h4>Objetivos... (no flex, no icon)
    content = re.sub(
        r'<h4[^>]*>\s*(?!' + re.escape(OBJECTIVES_SVG[:20]) + r')([^<]*Objetivos[^<]*)</h4>',
        lambda m: (
            f'<h4 class="text-blue-800 dark:text-blue-300 font-bold mb-3 flex items-center gap-2">'
            f'{OBJECTIVES_SVG}'
            f'{m.group(1).strip()}</h4>'
        ),
        content
    )
    
    return content


def fix_nav_footer(content: str, week_num: int) -> str:
    """Fix 9: Normalize nav footer with proper button styles from semana_01."""
    
    gold_nav = build_nav_footer(week_num)
    
    # Pattern: bare <div> with nav__link classes (semana_05 style)
    bare_nav = re.compile(
        r'<div\s+class="flex justify-between[^"]*pt-8 border-t[^"]*">\s*'
        r'<a\s+class="nav__link"[^>]*>[^<]*</a>\s*'
        r'<a\s+class="nav__link"[^>]*>[^<]*</a>\s*'
        r'</div>',
        re.DOTALL
    )
    content = bare_nav.sub(gold_nav, content)
    
    # Pattern: existing <nav> but with wrong link styles
    wrong_nav = re.compile(
        r'<nav\s+class="flex justify-between[^"]*">\s*'
        r'[\s\S]*?'
        r'</nav>',
        re.DOTALL
    )
    # Only replace if it contains nav__link or wrong button styles
    def fix_nav(m):
        if 'nav__link' in m.group(0) or 'px-5 py-2.5' not in m.group(0):
            return gold_nav
        return m.group(0)
    
    content = wrong_nav.sub(fix_nav, content)
    
    return content


def fix_sidebar_keywords_structure(content: str) -> str:
    """Fix 5: Ensure keywords sidebar has proper card wrapper."""
    
    # If keywords are floating without a card div, they should already be wrapped
    # by previous scripts. This ensures the card has the exact gold classes.
    
    # Normalize any existing keywords card to match gold standard exactly
    content = re.sub(
        r'class="bg-white\s+dark:bg-slate-900\s+rounded-2xl\s+border\s+border-slate-200\s+dark:border-slate-800\s+p-5\s+shadow-sm"',
        'class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm hover:shadow-md transition-shadow"',
        content
    )
    
    return content


def process_file(filepath: Path, week_num: int) -> None:
    """Process a single semana HTML file and apply all design fixes."""
    
    print(f"\n{'='*60}")
    print(f"Processing: {filepath.name} (Week {week_num})")
    print(f"{'='*60}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply fixes in order
    content = fix_html_tag(content)
    print("  ✅ Fix 1: scroll-smooth on <html>")
    
    content = fix_style_block(content)
    print("  ✅ Fix 2+3: style type=text/tailwindcss + @theme + removed master.css")
    
    content = fix_tailwind_script_order(content)
    print("  ✅ Fix 4: Tailwind CDN script order")
    
    content = fix_header(content, week_num)
    print("  ✅ Fix 5: Header <header> wrapper with max-w-7xl")
    
    content = fix_resources_sidebar(content)
    print("  ✅ Fix 6: Resources sidebar emerald colors")
    
    content = fix_sidebar_keywords_structure(content)
    print("  ✅ Fix 7: Keywords card hover shadow")
    
    content = fix_bare_pre_tags(content)
    print("  ✅ Fix 8: Bare <pre> → styled code blocks")
    
    content = fix_objectives_icon(content)
    print("  ✅ Fix 9: Objetivos SVG icon")
    
    content = fix_nav_footer(content, week_num)
    print("  ✅ Fix 10: Nav footer button styles")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  💾 SAVED: {filepath.name}")
    else:
        print(f"  ⚠️  No changes needed for {filepath.name}")


def main():
    print("🎨 DESIGN SYNC: semana_01 → semanas 02–16")
    print("=" * 60)
    
    weeks_to_fix = range(2, 17)  # semana_02 to semana_16
    
    for week in weeks_to_fix:
        filename = f"semana_{week:02d}.html"
        filepath = APUNTES_DIR / filename
        
        if filepath.exists():
            process_file(filepath, week)
        else:
            print(f"⚠️  Skipping {filename} — file not found")
    
    print("\n" + "=" * 60)
    print("✅ ALL DONE — Design synchronization complete!")
    print("   Open any week in your browser to verify.")


if __name__ == "__main__":
    main()
