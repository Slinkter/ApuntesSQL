"""
optimize_m3.py — Batch HTML optimizer para ULima/Apuntes
=========================================================
Aplica transformaciones sistemáticas siguiendo Material Design 3 y Tailwind v4:
  1. Elimina atributos `class` duplicados en el mismo elemento
  2. Corrige clases Tailwind inválidas (slate-650 → slate-600, slate-350 → slate-400)
  3. Añade tokens M3 faltantes en el bloque @theme
  4. Corrige estructura HTML de tablas (añade <thead>)
  5. Limpia clases Tailwind triplicadas en cards
  6. Elimina secciones duplicadas en index.html
  7. Mejora spacing: section, article, canvas controls, heading wrappers
  8. Normaliza saltos de línea extra (más de 2 consecutivos → 1)
"""

import re
import os
import glob

# ─── Directorio de trabajo ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Tokens M3 a inyectar en @theme (si no existen ya) ───────────────────────
M3_THEME_TOKENS = """
            /* M3 custom color tokens */
            --color-slate-350: #94a3b8;
            --color-slate-650: #475569;
            --color-m3-primary: #6750A4;
            --color-m3-primary-dark: #D0BCFF;"""

# ─── Helper: eliminar clases duplicadas dentro de class="..." ─────────────────
def dedup_class_attr(value: str) -> str:
    """Elimina clases duplicadas dentro de un string de clases Tailwind."""
    seen = []
    for cls in value.split():
        if cls not in seen:
            seen.append(cls)
    return " ".join(seen)


def fix_duplicate_class_attrs(html: str) -> str:
    """
    Cuando un elemento tiene class="..." class="..." (dos atributos class),
    los fusiona en uno solo eliminando duplicados.
    """
    # Patrón: class="A" ... class="B" en el mismo tag de apertura
    def merge_classes(m):
        tag_content = m.group(0)
        # Extraer todos los valores de class="..."
        classes_found = re.findall(r'class="([^"]*)"', tag_content)
        if len(classes_found) <= 1:
            return tag_content
        merged = " ".join(classes_found)
        deduped = dedup_class_attr(merged)
        # Reemplazar primera ocurrencia, eliminar las demás
        result = re.sub(r'class="[^"]*"', f'class="{deduped}"', tag_content, count=1)
        result = re.sub(r'\s+class="[^"]*"', '', result)
        return result

    # Capturar tags de apertura completos (sin < anidados)
    tag_pattern = re.compile(r'<[a-zA-Z][^>]*class="[^"]*"[^>]*class="[^"]*"[^>]*>', re.DOTALL)
    return tag_pattern.sub(merge_classes, html)


# ─── Corregir clases Tailwind inválidas ──────────────────────────────────────
INVALID_CLASSES = {
    "text-slate-650":          "text-slate-600",
    "text-slate-350":          "text-slate-400",
    "dark:text-slate-350":     "dark:text-slate-400",
    "dark:text-slate-650":     "dark:text-slate-600",
    "border-slate-850":        "border-slate-800",
    "dark:bg-slate-850":       "dark:bg-slate-800",
}

def fix_invalid_classes(html: str) -> str:
    for bad, good in INVALID_CLASSES.items():
        # Solo reemplaza como clase Tailwind completa (word boundary)
        html = re.sub(r'\b' + re.escape(bad) + r'\b', good, html)
    return html


# ─── Limpiar clases duplicadas dentro de un class="..." ──────────────────────
def dedup_inline_classes(html: str) -> str:
    """Elimina clases repetidas dentro del valor de un mismo atributo class."""
    def fix_value(m):
        deduped = dedup_class_attr(m.group(1))
        return f'class="{deduped}"'
    return re.sub(r'class="([^"]+)"', fix_value, html)


# ─── Corregir estructura de tablas ───────────────────────────────────────────
def fix_table_structure(html: str) -> str:
    """
    Patrón actual (roto):
      <table ...>
        <th ...>            ← th directamente en table, actúa como thead wrapper incorrecto
          <tr><th>...</th><th>...</th></tr>
          <tbody>...</tbody>
        </th></table>       ← cierre incorrecto

    Resultado esperado (correcto):
      <table ...>
        <thead>
          <tr><th>...</th><th>...</th></tr>
        </thead>
        <tbody>...</tbody>
      </table>
    """
    # Paso 1: Reemplazar <th class="..."> que abre inmediatamente después de <table ...>
    # seguido de un <tr> (es el th-wrapper incorrecto)
    # Capturamos: grupo(1)=<table...>, grupo(2)=th tag completo
    def fix_table_opener(m):
        pre = m.group(1)   # <table ...>
        # th_tag = m.group(2)  ← descartado
        return f'{pre}\n<thead>'

    html = re.sub(
        r'(<table[^>]*>)(\s*<th\b[^>]*>)(\s*(?=<tr))',
        lambda m: f'{m.group(1)}\n<thead>',
        html
    )

    # Paso 2: </th></table> → </thead></table>
    html = re.sub(r'</th>\s*</table>', '</thead></table>', html)

    # Paso 3: Asegurar que el tbody venga correctamente después del thead
    html = re.sub(r'(</tr>\s*)(</thead>)\s*(<tbody)', r'\1\2\n\3', html)

    return html


# ─── Añadir tokens M3 en @theme si no existen ────────────────────────────────
def inject_m3_tokens(html: str) -> str:
    if "--color-slate-350" in html:
        return html  # Ya tiene los tokens
    # Buscar el bloque @theme { ... }
    def add_tokens(m):
        theme_block = m.group(0)
        # Insertar antes del cierre }
        closing_brace_pos = theme_block.rfind("}")
        return theme_block[:closing_brace_pos] + M3_THEME_TOKENS + "\n        " + theme_block[closing_brace_pos:]

    return re.sub(r'@theme\s*\{[^}]+\}', add_tokens, html, flags=re.DOTALL)


# ─── Añadir space-y-8 al article principal ────────────────────────────────────
def fix_article_spacing(html: str) -> str:
    """
    El <article class="prose dark:prose-invert max-w-none"> principal
    que envuelve las secciones debería tener `space-y-8` para separar secciones.
    """
    def add_space(m):
        attrs = m.group(1)
        if "space-y-" in attrs or "gap-" in attrs:
            return m.group(0)
        # Insertar space-y-8 al inicio de las clases
        new_attrs = re.sub(r'class="', 'class="space-y-8 ', attrs, count=1)
        return f'<article {new_attrs}>'

    # Solo el article con prose (el contenedor principal de contenido)
    return re.sub(
        r'<article (class="prose[^"]*")>',
        add_space,
        html
    )


# ─── Normalizar saltos de línea extra ────────────────────────────────────────
def fix_blank_lines(html: str) -> str:
    """Colapsa más de 2 líneas en blanco consecutivas a 1."""
    return re.sub(r'\n{3,}', '\n\n', html)


# ─── Corregir h2 dentro de flex container (quitar mt-8 relativo) ─────────────
def fix_h2_in_flex(html: str) -> str:
    """
    <div class="flex items-center gap-3 mb-4">
      <h2 class="... mt-8 mb-4 ..."> ← el mt-8 no tiene sentido dentro de flex container
    
    Reemplaza mt-8 por mt-0 en h2/h3/h4 que están inmediatamente dentro de un div flex.
    Usa grupo de captura en lugar de lookbehind variable (no compatible con re estándar).
    """
    def strip_mt_in_heading(m):
        flex_div = m.group(1)     # <div class="flex ...">
        whitespace = m.group(2)   # espacios/newlines
        heading = m.group(3)      # <h2/h3/h4 ...>
        fixed_heading = re.sub(r'\bmt-8\b', 'mt-0', heading)
        return flex_div + whitespace + fixed_heading

    # Capturar: <div class="flex ..."> + espacios + <h2/h3/h4 con mt-8>
    pattern = re.compile(
        r'(<div\s[^>]*class="[^"]*\bflex\b[^"]*"[^>]*>)'  # <div class="flex ...">
        r'(\s*)'                                             # whitespace/newlines
        r'(<h[234]\b[^>]*\bmt-8\b[^>]*>)',                 # <h2/h3/h4 con mt-8>
        re.DOTALL
    )
    return pattern.sub(strip_mt_in_heading, html)


# ─── Eliminar secciones completamente duplicadas (index.html) ────────────────
def remove_duplicate_lab_sections(html: str) -> str:
    """
    En index.html la sección "Laboratorios y Guías Extras" aparece 3 veces.
    Detectamos los bloques del 2do y 3er "Laboratorios" y los eliminamos.
    """
    marker = 'Laboratorios y Guías Extras'
    marker_divs = [m.start() for m in re.finditer(re.escape(marker), html)]

    if len(marker_divs) <= 1:
        return html  # Solo hay 1, no hace falta limpiar

    # Nos quedamos con la primera + última sección (la última tiene mejor markup)
    # Eliminamos todas las intermedias desde el 2do marcador hasta antes del último
    if len(marker_divs) >= 3:
        # Encontrar inicio del div contenedor que precede al 2do marcador
        # Buscamos el <div class="text-xs ... hacia atrás desde marker_divs[1]
        start_2nd = html.rfind('<div', 0, marker_divs[1])
        # Encontrar inicio del div contenedor del último marcador
        start_last = html.rfind('<div', 0, marker_divs[-1])
        # Eliminar todo entre start_2nd y start_last
        if start_2nd != -1 and start_last != -1 and start_2nd < start_last:
            html = html[:start_2nd] + html[start_last:]
    elif len(marker_divs) == 2:
        # Eliminar desde el 2do hasta el final de su grid
        start_2nd = html.rfind('<div', 0, marker_divs[1])
        # Encontrar el grid container que sigue (el div.grid después del header)
        # Buscar </div> que cierra el grid de la segunda sección
        # Estrategia: buscar el patrón de cierre del grid section
        # Contamos profundidad de divs
        if start_2nd != -1:
            depth = 0
            i = start_2nd
            while i < len(html):
                if html[i:i+4] == '<div':
                    depth += 1
                    i += 4
                elif html[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        end_2nd_section = i + 6
                        # Ahora incluir también el siguiente grid
                        # Buscar el siguiente div.grid
                        next_grid = html.find('<div class="grid', end_2nd_section)
                        if next_grid != -1:
                            depth2 = 0
                            j = next_grid
                            while j < len(html):
                                if html[j:j+4] == '<div':
                                    depth2 += 1
                                    j += 4
                                elif html[j:j+6] == '</div>':
                                    depth2 -= 1
                                    if depth2 == 0:
                                        html = html[:start_2nd] + html[j+6:]
                                        break
                                    else:
                                        j += 6
                                else:
                                    j += 1
                        break
                    else:
                        i += 6
                else:
                    i += 1
    return html


# ─── Corregir padding del body en index.html ─────────────────────────────────
def fix_index_body_padding(html: str) -> str:
    """
    El body de index.html tiene p-4 pb-20 md:p-12 que causa padding excesivo.
    Lo reemplazamos por px-4 md:px-8 py-6 md:py-10 pb-20 más controlado.
    """
    old_body = r'class="bg-slate-50 text-slate-850 dark:bg-slate-950 dark:text-slate-350 antialiased font-sans transition-colors duration-300 p-4 pb-20 md:p-12"'
    new_body = 'class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-300 antialiased font-sans transition-colors duration-300 px-4 md:px-8 py-6 md:py-10 pb-20"'
    return html.replace(old_body, new_body)


# ─── Añadir h3 spacing en cards de index ─────────────────────────────────────
def fix_card_h3_spacing(html: str) -> str:
    """
    En las cards: <h3><span ...>S01</span> Título</h3>
    Añadir gap y alinear el span badge con el texto.
    Si no tiene clases ya las añade.
    """
    def add_h3_classes(m):
        existing = m.group(1) or ""
        if "flex" in existing or "items-center" in existing:
            return m.group(0)
        return f'<h3 class="flex items-start gap-2 text-base font-bold text-slate-900 dark:text-white mb-2 leading-snug {existing}">'

    # h3 sin clase o con clase vacía dentro de cards
    html = re.sub(
        r'<h3(?:\s+class="([^"]*)")?>\s*<span class="px-2',
        lambda m: f'<h3 class="flex items-center gap-2 text-base font-bold text-slate-900 dark:text-white mb-2 leading-snug {m.group(1) or ""}"><span class="px-2',
        html
    )
    return html


# ─── Procesar un archivo HTML ─────────────────────────────────────────────────
def process_file(filepath: str, is_index: bool = False) -> tuple[int, list[str]]:
    """
    Procesa un archivo HTML y aplica todas las transformaciones.
    Retorna (bytes_delta, lista_de_cambios_aplicados).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original
    changes = []

    # 1. Fusionar y deduplicar atributos class="" duplicados en mismo tag
    html_new = fix_duplicate_class_attrs(html)
    if html_new != html:
        changes.append("✔ Fusionados atributos class='...' class='...' duplicados")
        html = html_new

    # 2. Deduplicar clases dentro de class="A A B A"
    html_new = dedup_inline_classes(html)
    if html_new != html:
        changes.append("✔ Eliminadas clases Tailwind duplicadas dentro de class='...'")
        html = html_new

    # 3. Corregir clases Tailwind inválidas
    html_new = fix_invalid_classes(html)
    if html_new != html:
        changes.append("✔ Clases inválidas corregidas (slate-650→slate-600, slate-350→slate-400)")
        html = html_new

    # 4. Inyectar tokens M3 en @theme
    html_new = inject_m3_tokens(html)
    if html_new != html:
        changes.append("✔ Tokens M3 (@theme) inyectados")
        html = html_new

    # 5. Corregir estructura de tablas
    html_new = fix_table_structure(html)
    if html_new != html:
        changes.append("✔ Estructura de tablas corregida (<thead> añadido)")
        html = html_new

    # 6. Añadir space-y-8 al article principal
    html_new = fix_article_spacing(html)
    if html_new != html:
        changes.append("✔ space-y-8 añadido al <article> principal")
        html = html_new

    # 7. Corregir mt-8 en h2 dentro de flex containers
    html_new = fix_h2_in_flex(html)
    if html_new != html:
        changes.append("✔ mt-8 → mt-0 en headings dentro de flex containers")
        html = html_new

    # 8. Transformaciones específicas de index.html
    if is_index:
        html_new = remove_duplicate_lab_sections(html)
        if html_new != html:
            changes.append("✔ Secciones 'Laboratorios' duplicadas eliminadas de index.html")
            html = html_new

        html_new = fix_index_body_padding(html)
        if html_new != html:
            changes.append("✔ Padding del body en index.html normalizado")
            html = html_new

    # 9. Normalizar saltos de línea extra
    html_new = fix_blank_lines(html)
    if html_new != html:
        changes.append("✔ Saltos de línea extra normalizados")
        html = html_new

    # Solo escribir si hubo cambios
    delta = 0
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        delta = len(html) - len(original)

    return delta, changes


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    html_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.html")))
    
    if not html_files:
        print("❌ No se encontraron archivos HTML en:", BASE_DIR)
        exit(1)

    total_files = 0
    total_changes = 0
    print(f"\n{'='*60}")
    print(f"  ULima/Apuntes — Optimizador M3 + Tailwind v4")
    print(f"{'='*60}")
    print(f"  Procesando {len(html_files)} archivos HTML...\n")

    for filepath in html_files:
        filename = os.path.basename(filepath)
        is_index = filename == "index.html"

        delta, changes = process_file(filepath, is_index=is_index)

        if changes:
            total_files += 1
            total_changes += len(changes)
            sign = "+" if delta >= 0 else ""
            print(f"  📄 {filename} ({sign}{delta:+d} bytes)")
            for c in changes:
                print(f"     {c}")
            print()
        else:
            print(f"  ✅ {filename} — sin cambios necesarios")

    print(f"\n{'='*60}")
    print(f"  ✅ Completado: {total_files} archivos modificados, {total_changes} transformaciones")
    print(f"{'='*60}\n")
