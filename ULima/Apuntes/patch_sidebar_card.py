#!/usr/bin/env python3
"""
patch_sidebar_card.py
Wraps bare sidebar content (keywords + resources) that are missing the card div wrapper.
Targets files where the aside has <h2> directly without the bg-white card container.
"""

import re
from pathlib import Path

APUNTES_DIR = Path(__file__).parent

def patch_sidebar(content: str, week_num: int) -> str:
    """
    Finds aside sections where keywords and resources are bare (no card wrapper),
    and wraps them in proper card divs matching semana_01 gold standard.
    """
    
    # Build the gold standard resources card
    prev_link = "index.html" if week_num <= 2 else f"semana_{week_num-1:02d}.html"
    prev_text = "Semana Anterior (Inicio)" if week_num <= 2 else f"← Semana Anterior"
    next_link = f"semana_{week_num+1:02d}.html" if week_num < 16 else "index.html"
    next_text = f"Siguiente Semana →" if week_num < 16 else "Volver al Índice"

    # Pattern: <aside> containing bare <h2>Conceptos Clave / Palabras Clave</h2> + <ul> WITHOUT a wrapping card div
    # We detect by checking if aside has <h2> directly inside (not inside a div.bg-white)
    
    # Pattern to find the bare keywords section in aside
    bare_keywords_pattern = re.compile(
        r'(<aside[^>]*>)\s*\n'
        r'(<h2[^>]*>(?:Conceptos Clave|Palabras Clave|Temas Evaluados)[^<]*</h2>\s*\n'
        r'<ul[^>]*>[\s\S]*?</ul>)\s*\n'
        r'(<h2[^>]*>(?:Recursos)[^<]*</h2>\s*\n'
        r'<ul[^>]*>[\s\S]*?</ul>)\s*\n'
        r'(</aside>)',
        re.DOTALL
    )
    
    def wrap_sidebar(m):
        aside_open = m.group(1)
        keywords_block = m.group(2)
        resources_block = m.group(3)
        aside_close = m.group(4)
        
        # Extract h2 title from keywords
        kw_title_match = re.search(r'<h2[^>]*>([^<]*)</h2>', keywords_block)
        kw_title = kw_title_match.group(1).strip() if kw_title_match else "Palabras Clave"
        
        # Extract ul content from keywords  
        kw_ul_match = re.search(r'(<ul[^>]*>[\s\S]*?</ul>)', keywords_block)
        kw_ul = kw_ul_match.group(1) if kw_ul_match else ""
        
        # Extract ul content from resources
        res_ul_match = re.search(r'(<ul[^>]*>[\s\S]*?</ul>)', resources_block)
        res_ul = res_ul_match.group(1) if res_ul_match else ""

        return (
            f'{aside_open}\n'
            f'        <!-- Keywords -->\n'
            f'        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm hover:shadow-md transition-shadow">\n'
            f'            <h3 class="text-xs font-bold tracking-wider text-slate-400 dark:text-slate-500 uppercase mb-4">{kw_title}</h3>\n'
            f'            {kw_ul}\n'
            f'        </div>\n\n'
            f'        <!-- Resources -->\n'
            f'        <div class="bg-emerald-50 dark:bg-emerald-950/30 rounded-2xl border border-emerald-100 dark:border-emerald-900/50 p-5">\n'
            f'            <h3 class="text-xs font-bold tracking-wider text-emerald-600 dark:text-emerald-500 uppercase mb-4">Recursos</h3>\n'
            f'            <ul class="space-y-3 text-sm font-medium">\n'
            f'                <li><a href="index.html" class="text-emerald-700 dark:text-emerald-400 hover:text-emerald-500 transition-colors flex items-center gap-2">&larr; Inicio — Índice del Curso</a></li>\n'
            f'                <li><a href="{prev_link}" class="text-emerald-700 dark:text-emerald-400 hover:text-emerald-500 transition-colors flex items-center gap-2">{prev_text}</a></li>\n'
            f'                <li><a href="{next_link}" class="text-emerald-700 dark:text-emerald-400 hover:text-emerald-500 transition-colors flex items-center gap-2">{next_text}</a></li>\n'
            f'            </ul>\n'
            f'        </div>\n'
            f'    {aside_close}'
        )
    
    content = bare_keywords_pattern.sub(wrap_sidebar, content)
    return content


def process_file(filepath: Path, week_num: int) -> None:
    print(f"Patching sidebar: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = patch_sidebar(content, week_num)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  💾 SAVED: {filepath.name}")
    else:
        print(f"  ⚠️  No sidebar fix needed for {filepath.name}")


def main():
    print("🔧 PATCH: Sidebar card wrapper for bare keyword sections")
    print("=" * 60)
    
    # Only fix files identified with the bare sidebar pattern
    target_weeks = list(range(2, 17))
    
    for week in target_weeks:
        filename = f"semana_{week:02d}.html"
        filepath = APUNTES_DIR / filename
        if filepath.exists():
            process_file(filepath, week)
    
    print("\n✅ Sidebar patch complete!")


if __name__ == "__main__":
    main()
