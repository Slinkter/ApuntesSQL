import re

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

lab_count = idx.count('Laboratorios y')
dup_class = len(re.findall(r'dark:bg-slate-900 dark:bg-slate-900', idx))
invalid_cls = len(re.findall(r'text-slate-650|text-slate-350', idx))

print("=== index.html ===")
print(f"  Secciones Laboratorios:  {lab_count} (esperado: 1)")
print(f"  Clases dark duplicadas:  {dup_class} (esperado: 0)")
print(f"  Clases invalidas:        {invalid_cls} (esperado: 0)")

with open('semana_01.html', 'r', encoding='utf-8') as f:
    s01 = f.read()

thead_count = s01.count('<thead>')
broken_th   = len(re.findall(r'<table[^>]*>\s*<th\b', s01))
dup_cls_attr = len(re.findall(r'class="[^"]+" class="', s01))
space_y8    = s01.count('space-y-8')
invalid_cls2 = len(re.findall(r'text-slate-650|text-slate-350', s01))
m3_tokens = s01.count('--color-slate-350')

print("")
print("=== semana_01.html ===")
print(f"  <thead> elementos:       {thead_count} (esperado: >0)")
print(f"  <th> fuera de <thead>:   {broken_th} (esperado: 0)")
print(f"  class dobles en tags:    {dup_cls_attr} (esperado: 0)")
print(f"  space-y-8 en article:    {space_y8} (esperado: >=1)")
print(f"  Clases invalidas:        {invalid_cls2} (esperado: 0)")
print(f"  Tokens M3 en @theme:     {m3_tokens} (esperado: 1)")
