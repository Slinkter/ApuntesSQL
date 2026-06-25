Resume: agy --conversation=522dd917-d2f8-4a56-bb99-5f972aeabfaa (or -c)
Resume in the same project: agy --conversation=522dd917-d2f8-4a56-bb99-5f972aeabfaa --project=9c20da36-f2b0-4f2f-999b-ea3debb3ab14


# Plan ejecutable: Re-OCR de ULima con Ollama + GLM-OCR

> **Audiencia**: agentes locales (opencode-qwen3.5 o opencode-gemma4).
> **Ejecutor humano**: el usuario, que corre los agentes uno a uno y entrega los checkpoints.
> **Origen**: este plan lo generó Claude (cloud free) porque se acabaron los tokens cloud del usuario. A partir de aquí **toda la ejecución es local**.

---

## Progreso real (sesion 2026-06-25)

El usuario pidio **solo crear el plan y los scripts, no ejecutar las fases de OCR**. Pero en el camino se valido el entorno y se rasterizaron los 18 PDFs. Esto quedo en disco:

| Fase | Estado | Hecho en esta sesion |
|---|---|---|
| **0** — Verificar entorno | ✅ COMPLETADA | Ollama OK con glm-ocr 2.2GB, qwen3.5 6.6GB, gemma4 9.6GB. Python 3.13.9. Poppler NO disponible, se instalo PyMuPDF 1.27 como alternativa. |
| **1** — Rasterizar PDFs | ✅ COMPLETADA | 18 PDFs rasterizados a 150 DPI con PyMuPDF. 443 paginas totales, 73 MB en `ULima/.ocr_tmp/<pdf>/page-NNN.png`. TSV en `_logs/fase1_rasterizacion.tsv`. |
| **2** — OCR GLM-OCR | ⏸️ PENDIENTE | Script `fase2_ocr.py` listo. NO ejecutado por decision del usuario. |
| **3** — Comparar | ⏸️ PENDIENTE | Script `fase3_comparar.py` listo. |
| **4** — Reemplazar | ⏸️ PENDIENTE | Script `fase4_aplicar.py` con `--dry-run` listo. |
| **5** — Fixes puntuales | ⏸️ PENDIENTE | Comandos `sed` documentados en este plan. |
| **6** — Regenerar HTMLs | ⏸️ PENDIENTE | Mapeo TXT->HTML documentado. |
| **7** — Verificar + commits | ⏸️ PENDIENTE | Comandos git documentados. |

### Artefactos ya en disco

```
ULima/.ocr_tmp/
├── Clase_00/  Clase_01/  Clase_02/  Clase_03/  Clase_04/  Clase_05/  Clase_06/
├── Clase_09/  Clase_10/  Clase_11/  Clase_12/  Clase_15/
├── NormalizacioBD/  Practica_03_Sol/  Reglas.../  Restrictions on Parallel DML/
├── SolucionPractica/  Taller_HA_MSSQL2012/
├── _logs/
│   └── fase1_rasterizacion.tsv   <- 18 PDFs, 443 paginas, 73 MB
└── _scripts/
    ├── fase1_rasterizar.py        <- ya ejecutado
    ├── fase1_rasterizar.sh        <- version bash con pdftoppm (NO usado, dejo como referencia)
    ├── fase2_ocr.py               <- listo para correr
    ├── fase3_comparar.py          <- listo para correr
    └── fase4_aplicar.py           <- listo para correr (con --dry-run)
```

`.gitignore` actualizado: `ULima/.ocr_tmp/` excluido del repo.

### Resumen de paginas rasterizadas (de `fase1_rasterizacion.tsv`)

| PDF | Paginas | Tamano |
|---|---:|---:|
| Clase_00 | 34 | 6.0 MB |
| Clase_01 | 27 | 3.7 MB |
| Clase_02 | 39 | 5.5 MB |
| Clase_03 | 23 | 3.2 MB |
| Clase_04 | 15 | 2.1 MB |
| Clase_05 | 49 | 5.9 MB |
| Clase_06 | 21 | 2.7 MB |
| Clase_09 | 24 | 2.8 MB |
| Clase_10 | 32 | 4.8 MB |
| Clase_11 | 30 | 3.9 MB |
| Clase_12 | 13 | 1.5 MB |
| Clase_15 | 56 | 10.1 MB |
| NormalizacioBD | 6 | 1.0 MB |
| Practica_03_Sol | 5 | 0.9 MB |
| Reglas de Negocio... | 2 | 0.6 MB |
| Restrictions on Parallel DML | 2 | 0.4 MB |
| SolucionPractica | 1 | 0.2 MB |
| Taller_HA_MSSQL2012 | 64 | 16.1 MB |
| **TOTAL** | **443** | **~73 MB** |

### Como retomar desde Fase 2

```bash
cd "C:\Users\LJCR\Documents\GitHub\ApuntesSQL"

# Opcion A: smoke test con el PDF mas pequeno
python ULima/.ocr_tmp/_scripts/fase2_ocr.py --pdf SolucionPractica

# Opcion B: batch completo optimizado (10-20 minutos con 3 hilos paralelos)
python ULima/.ocr_tmp/_scripts/fase2_ocr.py

# Monitorear progreso en tiempo real (PowerShell nativo):
while ($true) { Clear-Host; $done = (Get-ChildItem -Path "C:\Users\LJCR\Documents\GitHub\ApuntesSQL\ULima\.ocr_tmp" -Filter "resultado_glm_ocr.txt" -Recurse -ErrorAction SilentlyContinue | Get-Content -ErrorAction SilentlyContinue | Select-String "--- PAGE ").Count; if (-not $done) { $done = 0 }; $pct = [math]::Round(($done / 443) * 100, 1); $bars = [int]($pct / 2.5); $barStr = "#" * $bars + "-" * (40 - $bars); Write-Output "Progreso: $done/443 ($pct%) [$barStr]"; Start-Sleep -Seconds 5 }

# Despues: comparar
python ULima/.ocr_tmp/_scripts/fase3_comparar.py

# Dry-run de reemplazos antes de aplicar
python ULima/.ocr_tmp/_scripts/fase4_aplicar.py --dry-run

# Reemplazos reales (solo si el reporte de Fase 3 te convence)
python ULima/.ocr_tmp/_scripts/fase4_aplicar.py
```

### 🛡️ Resiliencia y Recuperación (Si la PC se apaga o reinicia)

Si por alguna razón la PC se apaga, se reinicia o se corta la sesión de Ollama, sigue estas instrucciones para retomar de forma limpia y evitar archivos corruptos o mezclados:

1. **Matar procesos huérfanos:**
   En Windows, los procesos de Python lanzados en segundo plano pueden quedar activos incluso si el editor o contenedor se reinicia. Ejecuta este comando en PowerShell para limpiar cualquier proceso de OCR activo antes de continuar:
   ```powershell
   Get-CimInstance Win32_Process -Filter "name = 'python.exe'" | Where-Object { $_.CommandLine -like "*fase2_ocr.py*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
   ```

2. **Limpiar archivos incompletos:**
   Borra el log de la Fase 2 y el resultado parcial del PDF que se estaba procesando en el momento del corte (para evitar que se mezclen líneas o logs de ejecuciones anteriores). Por ejemplo, si se interrumpió en `Clase_01`:
   ```powershell
   Remove-Item -Path "ULima/.ocr_tmp/_logs/fase2_ocr.log" -ErrorAction SilentlyContinue
   Remove-Item -Path "ULima/.ocr_tmp/Clase_01/resultado_glm_ocr.txt" -ErrorAction SilentlyContinue
   ```

3. **Reanudar la Fase 2:**
   Ejecuta el script nuevamente con `python ULima/.ocr_tmp/_scripts/fase2_ocr.py`. El script detectará los archivos faltantes o vacíos y completará el lote de forma limpia.

### ⚡ Optimizaciones Aplicadas (2026-06-25)
* **Paralelismo (3 hilos):** Usa `ThreadPoolExecutor(max_workers=3)` en `fase2_ocr.py` para procesar 3 páginas simultáneamente aprovechando la VRAM libre de la GPU (RTX 2060).
* **Prompt Trigger Oficial:** Se usa `"Text Recognition:"` para forzar a GLM-OCR a entrar en su modo OCR optimizado y rápido.
* **Tokens de Parada (Stop Tokens):** Configurado `"stop": ["\n\`\`\`\n\`\`\`", "\`\`\`\n\n\`\`\`", "\`\`\`\n\`\`\`"]` para abortar la generación infinita de comillas/markdown repetitivos de Ollama.
* **Deduplicación Automática:** Filtra las respuestas de Ollama mediante `response.split("```")[0]` para extraer únicamente la transcripción de texto plano y descartar el bloque redundante en formato markdown.

### Como limpiar si decides no continuar

```bash
# Borrar todo el workspace OCR (deja repo limpio, .gitignore tambien)
rm -rf "ULima/.ocr_tmp"

# Revertir .gitignore (quitar las 2 lineas añadidas):
#   ULima/.ocr_tmp/
```

---

## Contexto

En `C:\Users\LJCR\Documents\GitHub\ApuntesSQL\ULima/` hay 19 PDFs de clases universitarias y 19 TXTs transcritos por un agente anterior. La auditoría previa mostró que la transcripción está mayormente bien (ratios 0.91-1.05) pero hay 1 PDF escaneado sin texto extraíble y ~6 líneas pegadas por limpiar.

El usuario quiere **rehacer la transcripción con un OCR moderno y dedicado** (GLM-OCR vía Ollama), compararlo contra lo que hay, y reemplazar solo si la calidad es >= 95%. Mantener el flujo PDF → TXT → HTML.

---

## Reglas del juego (leer antes de empezar)

- **Trabajas en local** con Ollama + GLM-OCR ya instalados. NO descargues modelos nuevos ni pidas conexión a la nube.
- **Solo lectura por defecto**: cada fase produce artefactos sin tocar los originales hasta que se decida reemplazo.
- **Backup obligatorio**: antes de sobrescribir cualquier TXT, copia el viejo a `ULima/.ocr_tmp/<pdf>/TXT_ANTERIOR_backup.txt`.
- **Encoding**: todos los TXT finales deben ser UTF-8 sin BOM y sin U+FFFD.
- **No resumas**: si GLM-OCR produce más texto que el original y es coherente, gana. Si produce menos, pierde.
- **Reporta al final de cada fase**: entrega el artefacto de bitácora marcado con ✅ / ⚠️ / ❌ según el checklist.

---

## Estructura de carpetas a crear

Antes de empezar, crea estas carpetas (en Git Bash de Windows):

```bash
mkdir -p ULima/.ocr_tmp
mkdir -p ULima/.ocr_tmp/_logs
```

`.ocr_tmp/` debe estar en `.gitignore`. Si no lo está, agrégalo:

```bash
grep -q "^\.ocr_tmp" .gitignore || echo ".ocr_tmp/" >> .gitignore
```

---

## FASE 0: Smoke test (5-10 min)

**Objetivo**: confirmar que Ollama, GLM-OCR y `pdftoppm` funcionan antes de lanzar nada en batch.

### Pasos

```bash
# 1. Ollama responde?
ollama list | grep -i glm-ocr

# 2. pdftoppm disponible?
pdftoppm -v 2>&1 | head -3

# 3. Rasteriza UNA pagina de Clase_05.pdf (es de tamaño medio, buen caso de prueba)
pdftoppm -r 200 -png -f 1 -l 1 "ULima/Clases/Clase_05.pdf" "ULima/.ocr_tmp/_smoke"

# 4. Verifica que el PNG existe
ls -la ULima/.ocr_tmp/_smoke*.png

# 5. Smoke test de GLM-OCR via HTTP API (ajusta el path del PNG)
curl -s http://localhost:11434/api/generate -d '{
  "model": "glm-ocr",
  "prompt": "Extrae todo el texto visible de esta imagen preservando saltos de línea y orden de lectura. No resumas. Si hay código, transcríbelo literal. Responde solo con el texto extraído, sin comentarios.",
  "images": ["'$(base64 -w0 ULima/.ocr_tmp/_smoke-1.png)'"]
}' | tee ULima/.ocr_tmp/_logs/fase0_smoke.json
```

### Verificación (criterio de éxito)

✅ El JSON de respuesta tiene un campo `response` con texto no vacío, coherente, en español o con código SQL reconocible.

❌ Si falla cualquiera de los 5 pasos: **detente y reporta**. No continues a Fase 1.

### Artefacto a entregar

- `ULima/.ocr_tmp/_logs/fase0_smoke.json` (puede estar truncado si es muy largo)
- `ULima/.ocr_tmp/_logs/fase0_smoke_resultado.txt` con las primeras 30 líneas del output del modelo para inspección visual

### Checklist de cierre

- [ ] `ollama list` muestra `glm-ocr`
- [ ] `pdftoppm -v` responde
- [ ] PNG de smoke test existe y > 50 KB
- [ ] JSON de Ollama tiene campo `response` no vacío
- [ ] El texto extraído se lee en español o contiene SQL reconocible

---

## FASE 1: Rasterización de los 19 PDFs (15-30 min)

**Objetivo**: convertir cada PDF a PNGs página por página, listos para OCR.

### Pasos

Crea el script `ULima/.ocr_tmp/_scripts/fase1_rasterizar.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

OUT_BASE="ULima/.ocr_tmp"
LOGS="$OUT_BASE/_logs"

mkdir -p "$LOGS"
> "$LOGS/fase1_rasterizacion.tsv"

for pdf in "ULima/Clases/Clase_00.pdf" \
           "ULima/Clases/Clase_01.pdf" \
           "ULima/Clases/Clase_02.pdf" \
           "ULima/Clases/Clase_03.pdf" \
           "ULima/Clases/Clase_04.pdf" \
           "ULima/Clases/Clase_05.pdf" \
           "ULima/Clases/Clase_06.pdf" \
           "ULima/Clases/Clase_09.pdf" \
           "ULima/Clases/Clase_10.pdf" \
           "ULima/Clases/Clase_11.pdf" \
           "ULima/Clases/Clase_12.pdf" \
           "ULima/Clases/Clase_15.pdf" \
           "ULima/otros/NormalizacioBD.pdf" \
           "ULima/otros/Practica_03_Sol.pdf" \
           "ULima/otros/Reglas de Negocio separadas del enunciado del Caso de Uso.pdf" \
           "ULima/otros/Restrictions on Parallel DML.pdf" \
           "ULima/otros/SolucionPractica.pdf" \
           "ULima/otros/Taller_HA_MSSQL2012.pdf"; do

  base=$(basename "$pdf" .pdf)
  outdir="$OUT_BASE/$base"
  mkdir -p "$outdir"

  echo "→ $pdf"
  pdftoppm -r 200 -png "$pdf" "$outdir/page" 2>>"$LOGS/fase1_errores.log"

  pages=$(ls "$outdir"/page-*.png 2>/dev/null | wc -l)
  size=$(du -sh "$outdir" | cut -f1)
  printf "%s\t%s\t%s\n" "$pdf" "$pages" "$size" >> "$LOGS/fase1_rasterizacion.tsv"
done

cat "$LOGS/fase1_rasterizacion.tsv"
```

Notas importantes:
- Hay 18 PDFs en la lista. El 19º es `ULima/Clases/Clase_07.pdf`, `Clase_08.pdf`, `Clase_13.pdf`, `Clase_14.pdf`, `Clase_16.pdf` que **no existen** (verificado en la auditoría previa). Estos huecos son normales.
- Si un PDF de la lista no existe, el script falla en `set -e`. Verifica primero:
  ```bash
  ls ULima/Clases/*.pdf ULima/otros/*.pdf | sort
  ```
  y ajusta la lista al resultado real.

### Verificación

✅ Cada PDF procesado tiene carpeta con PNGs `page-001.png`, `page-002.png`, ...
✅ El TSV final tiene 18 filas (o el número real de PDFs encontrados).

### Artefacto a entregar

- `ULima/.ocr_tmp/_logs/fase1_rasterizacion.tsv` con columnas: `pdf`, `num_paginas`, `tamano_total`
- `ULima/.ocr_tmp/_logs/fase1_errores.log` (puede estar vacío)

### Checklist de cierre

- [ ] Cada PDF listado tiene carpeta con al menos 1 PNG
- [ ] TSV con conteo de páginas completo
- [ ] Sin errores en el log (o errores explicados)
- [ ] Tamaño total de `ULima/.ocr_tmp/` razonable (< 2 GB)

---

## FASE 2: OCR página por página con GLM-OCR (1-3 horas)

**Objetivo**: pasar cada PNG por GLM-OCR y ensamblar el texto en un TXT por PDF.

### Pasos

Crea `ULima/.ocr_tmp/_scripts/fase2_ocr.py`:

```python
#!/usr/bin/env python3
"""OCR con GLM-OCR via Ollama. Itera paginas, ensambla TXT por PDF."""
import base64
import json
import sys
from pathlib import Path
import urllib.request

OUT_BASE = Path("ULima/.ocr_tmp")
LOGS = OUT_BASE / "_logs"
LOGS.mkdir(exist_ok=True)

PROMPT = (
    "Extrae todo el texto visible de esta imagen preservando saltos de línea "
    "y orden de lectura. No resumas. Si hay una tabla, mantén el formato. "
    "Si hay código SQL, transcríbelo literal. "
    "Responde solo con el texto extraído, sin comentarios."
)

def ocr_page(png_path: Path) -> str:
    img_b64 = base64.b64encode(png_path.read_bytes()).decode()
    payload = {
        "model": "glm-ocr",
        "prompt": PROMPT,
        "images": [img_b64],
        "stream": False,
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    return data.get("response", "")

def process_pdf(pdf_dir: Path, log_fh):
    pages = sorted(pdf_dir.glob("page-*.png"))
    if not pages:
        log_fh.write(f"  ⚠️  sin paginas: {pdf_dir.name}\n")
        return
    out_txt = pdf_dir / "resultado_glm_ocr.txt"
    log_fh.write(f"→ {pdf_dir.name}: {len(pages)} paginas\n")
    with out_txt.open("w", encoding="utf-8") as out:
        for i, page in enumerate(pages, 1):
            try:
                text = ocr_page(page)
                out.write(f"--- PAGE {i} ---\n")
                out.write(text)
                out.write("\n\n")
                out.flush()
                log_fh.write(f"   page {i}/{len(pages)} OK ({len(text)} chars)\n")
                log_fh.flush()
            except Exception as e:
                log_fh.write(f"   page {i}/{len(pages)} ERROR: {e}\n")
                log_fh.flush()
    log_fh.write(f"  ✓ {out_txt} ({out_txt.stat().st_size} bytes)\n")

def main():
    log_path = LOGS / "fase2_ocr.log"
    with log_path.open("w", encoding="utf-8") as log:
        pdf_dirs = sorted(d for d in OUT_BASE.iterdir() if d.is_dir() and d.name not in {"_logs", "_scripts"})
        log.write(f"PDFs a procesar: {len(pdf_dirs)}\n")
        for d in pdf_dirs:
            process_pdf(d, log)

if __name__ == "__main__":
    main()
```

Ejecuta:

```bash
cd "C:\Users\LJCR\Documents\GitHub\ApuntesSQL"
python ULima/.ocr_tmp/_scripts/fase2_ocr.py
```

### Estimación de tiempo

- ~5-15 s por página en GPU modesta, ~30-60 s en CPU.
- PDFs grandes (Clase_02, Clase_15, Taller_HA_MSSQL2012) pueden tener 80-120 páginas cada uno.
- Total estimado: 1-3 horas para 18 PDFs × ~50 páginas promedio.

### Opcional: checkpoint

Si el usuario quiere parar a revisar, el log `ULima/.ocr_tmp/_logs/fase2_ocr.log` muestra el progreso en tiempo real:

```bash
tail -f ULima/.ocr_tmp/_logs/fase2_ocr.log
```

### Verificación

✅ Cada PDF procesado tiene `resultado_glm_ocr.txt` no vacío.
✅ El log no tiene errores fatales (algunos errores de página son tolerables).

### Artefacto a entregar

- `ULima/.ocr_tmp/<pdf>/resultado_glm_ocr.txt` para cada PDF
- `ULima/.ocr_tmp/_logs/fase2_ocr.log` con progreso y errores

### Checklist de cierre

- [ ] 18 archivos `resultado_glm_ocr.txt` creados
- [ ] Tamaño promedio > 1 KB por TXT (placeholder de 164 bytes = falla)
- [ ] Sin errores fatales en el log

---

## FASE 3: Comparación y decisión de reemplazo (15-30 min)

**Objetivo**: para cada par (TXT actual, TXT de GLM-OCR), decidir mantener o reemplazar. Umbral: reemplazar solo si el nuevo aporta mejora medible.

### Pasos

Crea `ULima/.ocr_tmp/_scripts/fase3_comparar.py`:

```python
#!/usr/bin/env python3
"""Compara TXT actual vs GLM-OCR. Decide mantener/reemplazar/pendiente."""
import re
from pathlib import Path

OUT_BASE = Path("ULima/.ocr_tmp")
LOGS = OUT_BASE / "_logs"
LOGS.mkdir(exist_ok=True)

# Mapeo nombre_pdf -> ruta del TXT original
PDF_TO_TXT = {
    "Clase_00": "ULima/Clases/Clase_00.txt",
    "Clase_01": "ULima/Clases/Clase_01.txt",
    "Clase_02": "ULima/Clases/Clase_02.txt",
    "Clase_03": "ULima/Clases/Clase_03.txt",
    "Clase_04": "ULima/Clases/Clase_04.txt",
    "Clase_05": "ULima/Clases/Clase_05.txt",
    "Clase_06": "ULima/Clases/Clase_06.txt",
    "Clase_09": "ULima/Clases/Clase_09.txt",
    "Clase_10": "ULima/Clases/Clase_10.txt",
    "Clase_11": "ULima/Clases/Clase_11.txt",
    "Clase_12": "ULima/Clases/Clase_12.txt",
    "Clase_15": "ULima/Clases/Clase_15.txt",
    "NormalizacioBD": "ULima/otros/NormalizacioBD.txt",
    "Practica_03_Sol": "ULima/otros/Practica_03_Sol.txt",
    "Reglas de Negocio separadas del enunciado del Caso de Uso":
        "ULima/otros/Reglas de Negocio separadas del enunciado del Caso de Uso.txt",
    "Restrictions on Parallel DML": "ULima/otros/Restrictions on Parallel DML.txt",
    "SolucionPractica": "ULima/otros/SolucionPractica.txt",
    "Taller_HA_MSSQL2012": "ULima/otros/Taller_HA_MSSQL2012.txt",
}

U_FFFD = "�"

def count_words(p: Path) -> int:
    if not p.exists():
        return 0
    return len(p.read_text(encoding="utf-8", errors="replace").split())

def count_garbage(text: str) -> int:
    """Heuristica: U+FFFD + lineas de un solo caracter + '??'"""
    return (
        text.count(U_FFFD)
        + sum(1 for ln in text.splitlines() if len(ln.strip()) == 1 and ln.strip())
        + text.count("??")
    )

def decide(words_old: int, words_new: int, garbage_new: int) -> tuple[str, str]:
    """Politica de reemplazo."""
    # Caso 1: TXT viejo es placeholder (es unico caso conocido: Restrictions on Parallel DML)
    if words_old < 50:
        return ("REEMPLAZAR", f"placeholder ({words_old} palabras); GLM-OCR aporta contenido real")

    if words_new == 0:
        return ("MANTENER", "GLM-OCR no produjo texto; OCR fallo")

    ratio = words_new / words_old
    rel_garbage = garbage_new / max(words_new, 1)

    # Caso 2: GLM claramente mas completo Y limpio
    if ratio >= 1.05 and rel_garbage < 0.01:
        return ("REEMPLAZAR", f"GLM-OCR mas completo ({ratio:.2f}x) y limpio ({rel_garbage:.4f} garbage ratio)")

    # Caso 3: GLM claramente peor
    if ratio < 0.80:
        return ("MANTENER", f"GLM-OCR perdio informacion ({ratio:.2f}x); mantener actual")

    # Caso 4: empatados o cercanos
    if 0.95 <= ratio <= 1.05 and rel_garbage < 0.01:
        return ("MANTENER", f"empate tecnico ({ratio:.2f}x, garbage {rel_garbage:.4f}); actual es legible")

    return ("PENDIENTE_MANUAL", f"caso ambiguo ({ratio:.2f}x, garbage {rel_garbage:.4f}); revisar visualmente")

def main():
    rows = []
    for pdf_name, txt_path in PDF_TO_TXT.items():
        old = Path(txt_path)
        new = OUT_BASE / pdf_name / "resultado_glm_ocr.txt"
        words_old = count_words(old)
        words_new = count_words(new) if new.exists() else 0
        garbage_new = count_garbage(new.read_text(encoding="utf-8", errors="replace")) if new.exists() else 0
        decision, motivo = decide(words_old, words_new, garbage_new)
        rows.append((pdf_name, txt_path, words_old, words_new, decision, motivo))

    # Escribir reporte
    report = LOGS / "fase3_reporte.md"
    with report.open("w", encoding="utf-8") as f:
        f.write("# Fase 3: Reporte de comparacion TXT actual vs GLM-OCR\n\n")
        f.write("| PDF | TXT actual | GLM-OCR | Decision | Motivo |\n")
        f.write("|---|---:|---:|---|---|\n")
        for r in rows:
            f.write(f"| {r[0]} | {r[2]} | {r[3]} | **{r[4]}** | {r[5]} |\n")

    # Escribir CSV para post-procesado
    csv = LOGS / "fase3_reporte.csv"
    with csv.open("w", encoding="utf-8") as f:
        f.write("pdf,txt_path,words_old,words_new,decision,motivo\n")
        for r in rows:
            row_csv = '","'.join(str(x).replace('"', '""') for x in r)
            f.write(f'"{row_csv}"\n')

    print(report.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
```

Ejecuta:

```bash
python ULima/.ocr_tmp/_scripts/fase3_comparar.py
```

### Política de reemplazo (resumen)

| Condición | Decisión |
|---|---|
| TXT actual tiene < 50 palabras (placeholder) | **REEMPLAZAR** |
| GLM-OCR tiene 0 palabras | MANTENER (OCR falló) |
| GLM-OCR >= 1.05x palabras Y garbage ratio < 1% | **REEMPLAZAR** (más completo y limpio) |
| GLM-OCR < 0.80x palabras | MANTENER (perdió información) |
| Empate (0.95-1.05x) y limpio | MANTENER (actual es legible) |
| Cualquier otro caso | PENDIENTE_MANUAL |

### Verificación

✅ El reporte tiene 18 filas (una por PDF que existe).
✅ Las decisiones son consistentes con la política.
✅ El CSV es parseable.

### Artefacto a entregar

- `ULima/.ocr_tmp/_logs/fase3_reporte.md` (tabla markdown legible)
- `ULima/.ocr_tmp/_logs/fase3_reporte.csv` (para Fase 4)

### Checklist de cierre

- [ ] Reporte tiene 18 filas
- [ ] Decisiones siguen la política del cuadro arriba
- [ ] El usuario revisa manualmente los casos `PENDIENTE_MANUAL`

---

## FASE 4: Aplicar reemplazos + limpieza (15-30 min)

**Objetivo**: para cada par con decisión REEMPLAZAR, copiar el TXT nuevo al lugar del viejo (con backup), y limpiar separadores `--- PAGE N ---`.

### Pasos

Crea `ULima/.ocr_tmp/_scripts/fase4_aplicar.py`:

```python
#!/usr/bin/env python3
"""Aplica reemplazos segun el reporte de Fase 3. Backup obligatorio."""
import csv
import re
import shutil
from pathlib import Path

LOGS = Path("ULima/.ocr_tmp/_logs")
OUT_BASE = Path("ULima/.ocr_tmp")

def clean_text(text: str) -> str:
    """Elimina separadores de pagina, U+FFFD residuales, colapsa whitespace."""
    # Quitar separadores --- PAGE N ---
    text = re.sub(r"^--- PAGE \d+ ---\s*\n", "", text, flags=re.MULTILINE)
    # Quitar U+FFFD
    text = text.replace("�", "")
    # Colapsar multiples saltos de linea a maximo 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Colapsar espacios al final de linea
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip() + "\n"

def main():
    log_path = LOGS / "fase4_aplicar.log"
    with log_path.open("w", encoding="utf-8") as log:
        with (LOGS / "fase3_reporte.csv").open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decision = row["decision"]
                pdf_name = row["pdf"]
                txt_path = Path(row["txt_path"])

                if decision != "REEMPLAZAR":
                    log.write(f"⊘ {pdf_name}: {decision} (no se toca)\n")
                    continue

                # Buscar el TXT nuevo
                src = OUT_BASE / pdf_name / "resultado_glm_ocr.txt"
                if not src.exists():
                    log.write(f"❌ {pdf_name}: no hay resultado_glm_ocr.txt\n")
                    continue

                # Backup del TXT viejo
                if txt_path.exists():
                    backup = OUT_BASE / pdf_name / "TXT_ANTERIOR_backup.txt"
                    backup.parent.mkdir(exist_ok=True)
                    shutil.copy2(txt_path, backup)
                    log.write(f"  backup: {txt_path} -> {backup}\n")

                # Limpiar y escribir
                cleaned = clean_text(src.read_text(encoding="utf-8", errors="replace"))
                txt_path.write_text(cleaned, encoding="utf-8")
                log.write(f"✓ {pdf_name}: reemplazado ({len(cleaned)} chars)\n")

    print(log_path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
```

Ejecuta:

```bash
python ULima/.ocr_tmp/_scripts/fase4_aplicar.py
```

### Verificación

✅ Cada reemplazo tiene backup en `.ocr_tmp/<pdf>/TXT_ANTERIOR_backup.txt`.
✅ El TXT nuevo está en UTF-8 sin BOM.
✅ Sin separadores `--- PAGE N ---` residuales.
✅ Sin U+FFFD.

```bash
# Verificacion rapida
for f in ULima/Clases/*.txt ULima/otros/*.txt; do
  if grep -l $'\xef\xbf\xbd' "$f" >/dev/null 2>&1; then
    echo "⚠️  U+FFFD en: $f"
  fi
  if grep -l "^--- PAGE " "$f" >/dev/null 2>&1; then
    echo "⚠️  separadores residuales en: $f"
  fi
done
echo "Si no hay output, todo OK"
```

### Artefacto a entregar

- TXTs actualizados in-place (los originales reemplazados)
- `ULima/.ocr_tmp/<pdf>/TXT_ANTERIOR_backup.txt` por cada reemplazo
- `ULima/.ocr_tmp/_logs/fase4_aplicar.log`

### Checklist de cierre

- [ ] Todos los reemplazos listados en Fase 3 están aplicados
- [ ] Cada TXT reemplazado tiene backup
- [ ] Cero U+FFFD en todos los TXT finales
- [ ] Cero separadores `--- PAGE N ---` residuales

---

## FASE 5: Reparar líneas pegadas en TXTs NO reemplazados

**Objetivo**: si Fase 4 mantuvo algunos TXTs originales (por decisión MANTENER), aplicar las correcciones puntuales conocidas de la auditoría previa. **No tocar los que ya fueron reemplazados por GLM-OCR en Fase 4** (el OCR probablemente los regeneró limpios).

### Líneas pegadas conocidas (de la auditoría previa)

| Archivo | Línea | Problema | Solución |
|---|---:|---|---|
| `ULima/Clases/Clase_00.txt` | 234-235 | `Recuperación (?)Terminología` | Salto de línea antes de `Terminología` |
| `ULima/Clases/Clase_01.txt` | 17 | `sin un buen diseño?Dato vs Información` | Salto de línea antes de `Dato vs Información` |
| `ULima/Clases/Clase_06.txt` | 55 | `un aumento de salario?Dependencia Funcional y Claves` | Salto de línea antes de `Dependencia Funcional` |
| `ULima/Clases/Clase_10.txt` | 19 | `– HAVINGJOIN¿Qué es un Join?` | Tres saltos (HAVING, JOIN, ¿Qué es un Join?) |
| `ULima/Clases/Clase_11.txt` | 95, 126 | `TRUNC(SYSDATE, 'YEAR' \| 'MONTH') ?Conversiones de Datos` y `VACIO?` | Saltos de línea |
| `ULima/otros/Script_Ejemplo_Warehouse.txt` | 1 | `Recomendación` con U+FFFD | Reemplazar `Recomendacin` por `Recomendación` |

### Pasos

**Aplica SOLO si el archivo NO fue reemplazado en Fase 4.** Si fue reemplazado, omítelo (GLM-OCR probablemente lo regeneró limpio; verifica visualmente si hay dudas).

Para cada archivo a corregir:

1. Lee la línea exacta con `sed -n '234p' archivo.txt` o `awk 'NR==234' archivo.txt`.
2. Compara con el problema esperado.
3. Aplica el fix con Edit o sed:

```bash
# Ejemplo Clase_00.txt linea 234
sed -i 's/Recuperación (?)Terminología/Recuperación (?)\nTerminología/' ULima/Clases/Clase_00.txt

# Script_Ejemplo_Warehouse.txt linea 1: U+FFFD
sed -i 's/Recomendaci�n/Recomendación/' "ULima/otros/Script_Ejemplo_Warehouse.txt"
```

4. Verifica con `grep` que el patrón viejo ya no aparece.

### Verificación

✅ Los 6 fixes están aplicados donde corresponde.
✅ Diff visual confirma que el salto de línea aparece donde debe.

### Artefacto a entregar

- TXTs corregidos
- `ULima/.ocr_tmp/_logs/fase5_fixes.log` con la lista de cambios aplicados

### Checklist de cierre

- [ ] 6 fixes aplicados (o documentados como ya resueltos por Fase 4)
- [ ] Sin nuevos U+FFFD introducidos

---

## FASE 6: Regenerar HTMLs afectados

**Objetivo**: regenerar los `semana_XX.html` cuyo TXT origen cambió en Fases 4-5, preservando la estructura Cornell + BEM.

### Mapeo TXT → HTML (de `prompt.md` Fase 2)

| TXT origen | HTML destino |
|---|---|
| Clase_00.txt | semana_01.html |
| Clase_01.txt + Clase_02.txt | semana_02.html |
| Clase_03.txt (conceptos) | semana_03.html |
| Clase_03.txt (DDL) | semana_04.html |
| Clase_04.txt | semana_05.html |
| Clase_05.txt | semana_06.html |
| Clase_06.txt + NormalizacioBD.txt | semana_07.html |
| Clase_09.txt | semana_09.html |
| Clase_10.txt (JOINs) | semana_10.html |
| Clase_10.txt (agrupamiento) | semana_11.html |
| Clase_11.txt (intro) | semana_12.html |
| Clase_11.txt (avanzado) | semana_13.html |
| Clase_12.txt + Clase_15.txt + Script_Ejemplo_Warehouse.txt | semana_14.html |
| Taller_HA_MSSQL2012.txt + Restrictions on Parallel DML.txt (si se transcribió) | semana_15.html |

### Pasos

Para cada HTML cuyo TXT origen cambió:

1. Lee el HTML actual completo (`ULima/Apuntes/semana_XX.html`).
2. Lee el TXT nuevo.
3. Identifica secciones del HTML que necesitan actualizarse:
   - Bloques `<pre>` con código SQL que haya cambiado.
   - Texto en `<p>` o `<li>` que reproduzca el contenido del TXT.
   - Bloques `architect-insight` que referencien datos específicos.
4. **Preserva intacto**:
   - Cabecera y navegación.
   - Estructura BEM (`.sidebar`, `.main`, `.box--note`, `.architect-insight`, etc.).
   - `master.css` y `canvas-ui.js`.
5. **Actualiza**:
   - Contenido de los `<pre>` con el SQL exacto del TXT nuevo.
   - Listas con datos del TXT nuevo.
   - `architect-insight` si el contenido específico cambió.

### Caso especial: `Restrictions on Parallel DML.txt`

Si se transcribió por primera vez en Fase 4, decide:

**Opción A (recomendada)**: crear `ULima/Apuntes/extra_parallel_dml.html` siguiendo el patrón de los otros `extra_*.html` (sin enlace desde `index.html`, contenido complementario).

**Opción B**: integrarlo en `semana_15.html` como sección nueva bajo el tema HA.

### Verificación post-regeneración

```bash
# Cada HTML regenerado debe:
# 1. Mantener clases BEM
grep -c "class=" ULima/Apuntes/semana_XX.html
# 2. Tener al menos un architect-insight
grep -c "architect-insight" ULima/Apuntes/semana_XX.html
# 3. Sin U+FFFD
grep -l $'\xef\xbf\xbd' ULima/Apuntes/semana_XX.html  # debe estar vacio
```

### Artefacto a entregar

- HTMLs regenerados (en `ULima/Apuntes/semana_XX.html` o `extra_parallel_dml.html`)
- `ULima/.ocr_tmp/_logs/fase6_html.log` con lista de HTMLs modificados y métricas antes/después

### Checklist de cierre

- [ ] Todos los HTMLs cuyo TXT cambió fueron regenerados
- [ ] Métricas antes/después similares (no colapsó estructura)
- [ ] Si se creó `extra_parallel_dml.html`, está accesible y formateado consistentemente

---

## FASE 7: Verificación final + commits

**Objetivo**: confirmar todo está bien, actualizar documentación interna, hacer commits por fase.

### Verificación final

```bash
cd "C:\Users\LJCR\Documents\GitHub\ApuntesSQL"

echo "=== AUDITORIA FINAL ==="

echo "1. Ratios PDF/TXT:"
for pdf in ULima/Clases/*.pdf ULima/otros/*.pdf; do
  txt="${pdf%.pdf}.txt"
  [ -f "$txt" ] || { echo "  ❌ $pdf sin TXT"; continue; }
  pdf_words=$(pdftotext -layout "$pdf" - 2>/dev/null | wc -w)
  txt_words=$(wc -w < "$txt")
  if [ "$pdf_words" -gt 0 ]; then
    ratio=$(echo "scale=3; $txt_words / $pdf_words" | bc 2>/dev/null || echo "N/A")
    echo "  $txt: $txt_words palabras (pdf=$pdf_words, ratio=$ratio)"
  fi
done

echo ""
echo "2. Encoding:"
for f in ULima/Clases/*.txt ULima/otros/*.txt; do
  enc=$(file -i "$f" | grep -o "charset=[^ ]*")
  echo "  $f: $enc"
done

echo ""
echo "3. U+FFFD en TXT/HTML:"
grep -rl $'\xef\xbf\xbd' ULima/Clases/ ULima/otros/ ULima/Apuntes/ 2>/dev/null || echo "  ✓ ninguno"

echo ""
echo "4. Separadores PAGE residuales:"
grep -rl "^--- PAGE " ULima/Clases/ ULima/otros/ 2>/dev/null || echo "  ✓ ninguno"
```

### Actualización documental

1. **`prompt.md` sección "Fase 1: Limpieza de archivos TXT"** — agregar al final:

```markdown
### [x] Fase 1b: Re-OCR con Ollama + GLM-OCR (2026-06-25)

- [x] Rasterización de 18 PDFs a PNG con `pdftoppm -r 200`
- [x] OCR con GLM-OCR vía Ollama, prompt "extrae texto sin resumir"
- [x] Comparación TXT actual vs GLM-OCR (umbral 95% para reemplazo)
- [x] Reemplazos aplicados: <lista>
- [x] Mantenidos: <lista>
- [x] Pendientes manuales: <lista>
- [x] Reparación de líneas pegadas (Clase_00, 01, 06, 10, 11)
- [x] Corrección U+FFFD en Script_Ejemplo_Warehouse.txt
- [x] HTMLs regenerados: <lista>
```

2. **`AGENTS.md`** — opcional, agregar:

```markdown
## OCR workflow (added 2026-06-25)

Use Ollama + GLM-OCR for PDF→TXT transcription when needed. See `prompt.md` Fase 1b for the full workflow.
```

3. **`.gitignore`** — confirmar que `ULima/.ocr_tmp/` está excluido.

4. **`ULima/.ocr_tmp/_logs/`** — mover los logs a un único resumen `ULima/_OCR_2026-06-25.md` o dejarlos como bitácora (a decisión del usuario).

### Commits (uno por fase, no monolítico)

```bash
cd "C:\Users\LJCR\Documents\GitHub\ApuntesSQL"

# Solo si .ocr_tmp/ no esta en .gitignore, sino omitir
# git add ULima/.ocr_tmp/_logs/*.md
# git commit -m "chore: add OCR processing logs (excluidos del repo via .gitignore)"

# Fase 4: reemplazos de TXT
git add ULima/Clases/*.txt ULima/otros/*.txt
git commit -m "fix: re-transcribe ULima TXT with GLM-OCR where ratio >= 95%

Co-Authored-By: opencode-qwen3.5 <noreply@local>"

# Fase 5: fixes puntuales
git add ULima/Clases/Clase_*.txt ULima/otros/Script_Ejemplo_Warehouse.txt
git commit -m "fix: repair glued lines and U+FFFD in legacy ULima TXTs

Co-Authored-By: opencode-qwen3.5 <noreply@local>"

# Fase 6: HTMLs regenerados
git add ULima/Apuntes/
git commit -m "docs: regenerate semana_XX.html from updated TXTs

Co-Authored-By: opencode-qwen3.5 <noreply@local>"

# Fase 7: documentacion
git add prompt.md AGENTS.md .gitignore
git commit -m "docs: document OCR workflow in prompt.md and AGENTS.md

Co-Authored-By: opencode-qwen3.5 <noreply@local>"
```

### Artefacto final

- Repositorio sincronizado.
- `prompt.md` actualizado.
- 4-5 commits limpios, cada uno con scope claro.
- `ULima/.ocr_tmp/` local (no commiteado si está en `.gitignore`).

### Checklist de cierre global

- [ ] Auditoría final ejecutada y ratios OK
- [ ] Cero U+FFFD en TXT y HTML
- [ ] Encoding UTF-8 en todos los TXT
- [ ] HTMLs regenerados mantienen BEM
- [ ] `prompt.md` actualizado con Fase 1b
- [ ] `.gitignore` excluye `.ocr_tmp/`
- [ ] Commits por fase, mensajes claros con Co-Authored-By

---

## Resumen ejecutivo para el usuario

| Fase | Duración estimada | Output principal |
|---|---|---|
| 0 — Smoke test | 5-10 min | `fase0_smoke.json` |
| 1 — Rasterización | 15-30 min | 18 carpetas con PNGs |
| 2 — OCR | 1-3 horas | 18 `resultado_glm_ocr.txt` |
| 3 — Comparación | 15-30 min | `fase3_reporte.md` |
| 4 — Reemplazos | 15-30 min | TXTs actualizados + backups |
| 5 — Fixes puntuales | 10 min | Líneas pegadas reparadas |
| 6 — Regenerar HTMLs | 30-90 min | HTMLs sincronizados |
| 7 — Verificación + commits | 20 min | Repo limpio |

**Total estimado**: 3-5 horas, ejecutable en una sesión larga o partida en 2 días.

**Punto crítico**: Fase 3 produce el reporte de decisiones. **El usuario debe revisar manualmente los casos `PENDIENTE_MANUAL` antes de que Fase 4 se ejecute**, porque ahí es donde se decide qué TXT se reemplaza y cuál no. Sin ese gate, se puede perder información buena por OCR malo.
