# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import markdown
import os
import re
from sys import platform


__all__ = [""]


def convhtml(text: str, filename: str, font: str, ckb: bool = False):
    # Converting your TVG to html and printable directly from browser.
    
    try:
        if os.path.isfile(text):
            with open(text) as rdf:
                gettext = rdf.readlines()
        else:
            gettext = text.split('\n')
            
        tohtml = []
        for i in gettext:
            if i != '\n':
                sp = re.match(r'\s+', i)
                if sp:
                    sp = sp.span()[1]-4
                    txt = re.search(r'-', i)
                    if txt and not i[txt.span()[1]:].isspace():
                        txt = f'* {i[txt.span()[1]:]}'
                    else:
                        txt = '*  '
                    tohtml.append(f'{" " * sp}{txt}\n\n')
                else:
                    if '\n' in i and re.search(r'\w+', i):
                        tohtml.append(f'#### {i}\n')
                    elif re.search(r'\w+', i):
                        tohtml.append(f'#### {i}\n\n')
        chg = f"""{''.join(tohtml)}"""
        a  = markdown.markdown(chg)
        setfont = 'body { ' + f"""background-color: gold;
  font:{font};""" + ' }'
        checkbut = """.task-list-item {
  list-style-type: none !important;
}
.task-list-item input[type="checkbox"] {
  margin: 0 4px 0.25em -20px;
  vertical-align: middle;
}
.strikethrough:checked + span {
  text-decoration: line-through;
}
"""
        cssstyle = f"""<!DOCTYPE html>
<html>
<button class="button"  onclick="javascript:window.print();">Print</button>
<header>
<h1>
<strong>
{filename}
</strong>
</h1>
</header>
<style>
{setfont}
"""
        printed = """@media print {
.button { display: none }
}
</style>
<body>
"""
        nxt = f"""{a}
</body>
</html>
"""
        if ckb:
            cssstyle = cssstyle + checkbut + printed + nxt
            cs = cssstyle.split('\n')
            fcs = []
            for i in cs:
                if '<li>' in i and len(i) > 5:
                    fx = i[:4]+'\n<p>\n<span>'+i[4:-5]+'</span>\n</p>\n'+i[-5:]+'\n'
                    fcs.append(fx)
                elif '<p>' in i:
                    fx = i[:3]+'\n<span>'+i[3:-4]+'</span>\n'+i[-4:]+'\n'
                    fcs.append(fx)
                else:
                    fcs.append(f'{i}\n')
            del cs
            cssstyle = ''.join(fcs)
            cssstyle = cssstyle.replace('<ul>', '<ul class="task-list">')
            cssstyle = cssstyle.replace('<li>', '<li class="task-list-item">')
            cssstyle = cssstyle.replace('<p>','<p><input type="checkbox" class="strikethrough" name="ck"/>')
            cssstyle = cssstyle.replace('<span>','<span for="ck">')
            del fcs
        else:
            cssstyle = cssstyle + printed + nxt
        with open(f'{filename}.html', 'w') as whtm:
            whtm.write(cssstyle)
        if platform.startswith('win'):
            os.startfile(f'{filename}.html')
        else:
            os.system(f'open "{filename}.html"')
    except Exception as e:
        raise e