# -*- coding: utf-8 -*-
"""
Assembles all sections into 2.Ejercicios/4.examen_entrevista.md
"""

import os
import sys

from make_examen import header
from sec1_3 import sec1_3_text
from sec4_6 import sec4_6_text
from sec7_9 import sec7_9_text

target_file = r"C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md"

full_content = header.strip() + "\n\n" + sec1_3_text.strip() + "\n\n" + sec4_6_text.strip() + "\n\n" + sec7_9_text.strip() + "\n"

with open(target_file, "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully assembled {target_file}")
print(f"Total size: {len(full_content)} characters / {os.path.getsize(target_file)} bytes")
