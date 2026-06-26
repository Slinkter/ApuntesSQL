import os
import glob
import re

os.chdir(r'C:\Users\LJCR\Documents\GitHub\ApuntesSQL\ULima\Apuntes')

replacements = {
    # Layout & Structural
    '<body': '<body class="bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-300 antialiased font-sans transition-colors duration-300"',
    'class="header"': 'class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50 shadow-sm"',
    'class="header__title"': 'class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white"',
    'class="header__subtitle"': 'class="mt-2 text-sm font-medium text-slate-500 dark:text-slate-400"',
    'class="cornell"': 'class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col md:flex-row gap-8"',
    'class="sidebar"': 'class="w-full md:w-1/3 lg:w-1/4 flex flex-col gap-6 shrink-0"',
    'class="sidebar__title"': 'class="text-xs font-bold tracking-wider text-slate-400 dark:text-slate-500 uppercase mb-4"',
    'class="sidebar__list"': 'class="space-y-4"',
    'class="sidebar__item"': 'class="text-sm"',
    'class="main"': 'class="w-full md:w-2/3 lg:w-3/4 flex flex-col gap-10 pb-20"',
    
    # Typography
    'class="main__title"': 'class="text-2xl font-bold text-slate-900 dark:text-white mb-4"',
    'class="main__title--sub"': 'class="text-xl font-bold text-slate-900 dark:text-white mb-3"',
    'class="main__text"': 'class="text-slate-700 dark:text-slate-300 leading-relaxed mb-4"',
    'class="main__list"': 'class="space-y-3 mb-6 pl-5 list-disc text-slate-700 dark:text-slate-300"',
    'class="main__list-item"': '',
    
    # Components
    'class="tag"': 'class="inline-block px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 mb-4"',
    'class="architect-insight"': 'class="pl-4 border-l-4 border-amber-500 dark:border-amber-600 mb-6"',
    
    # Boxes / Callouts
    'class="box box--note"': 'class="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6 border border-blue-100 dark:border-blue-800/50 mb-6"',
    'class="box box--concept"': 'class="bg-indigo-50 dark:bg-indigo-900/20 rounded-xl p-5 border border-indigo-100 dark:border-indigo-800/50 mb-6"',
    'class="box box--warning"': 'class="bg-rose-50 dark:bg-rose-900/20 rounded-xl p-5 border border-rose-100 dark:border-rose-800/50 mb-6"',
    'class="box box--exercise"': 'class="bg-fuchsia-50 dark:bg-fuchsia-900/20 rounded-2xl p-6 border border-fuchsia-100 dark:border-fuchsia-800/50 mb-6"',
    'class="box box--example"': 'class="bg-slate-100 dark:bg-slate-800/50 rounded-xl p-5 border border-slate-200 dark:border-slate-700 mb-6"',
    
    # Tables
    'class="table-responsive"': 'class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm mb-6"',
    'class="table"': 'class="w-full text-left border-collapse"',
    'class="table__th"': 'class="p-4 border-b border-slate-200 dark:border-slate-700 font-semibold text-slate-900 dark:text-slate-100"',
    'class="table__td"': 'class="p-4 text-slate-600 dark:text-slate-400"',
    
    # Navigation
    'class="nav"': 'class="flex justify-between items-center pt-8 border-t border-slate-200 dark:border-slate-800 mt-8"',
}

# Regex for table rows since they might need specific classes based on location (thead vs tbody is tricky, we'll apply a generic hover row style)
tr_pattern = re.compile(r'class="table__tr"')

files = [f'semana_{str(i).zfill(2)}.html' for i in range(2, 9)]

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements.items():
            # Basic string replace
            content = content.replace(old, new)
            
        # Specific Tr replacement
        content = tr_pattern.sub('class="bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"', content)
        
        # specific sidebar fixes for active states
        content = content.replace('class="sidebar__link"', 'class="text-emerald-700 dark:text-emerald-400 hover:text-emerald-500 transition-colors"')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Refactored {file}")
