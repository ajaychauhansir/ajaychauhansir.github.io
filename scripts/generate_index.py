import os, html
from urllib.parse import quote

BASE = "BCom"
SEMS = {"Sem-3": "3", "Sem-5": "5"}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>B.Com Semester __SEM__ - __YEAR__ Question Papers | Ajay Chauhan</title>
<link rel="stylesheet" href="/css/style.css">
<style>
.pdf-list{max-width:800px;margin:50px auto 80px;padding:0 20px}
.pdf-row{display:flex;align-items:center;gap:14px;background:white;border:1px solid #e5e7eb;border-left:5px solid #2563eb;border-radius:12px;padding:16px 18px;margin-bottom:12px;text-decoration:none;color:#1f2937;box-shadow:0 4px 14px rgba(15,23,42,0.06);transition:.2s}
.pdf-row:hover{transform:translateX(4px);box-shadow:0 8px 22px rgba(15,23,42,0.12)}
.pdf-icon{font-size:26px}
.pdf-name{flex:1;font-size:16px;font-weight:600;color:#172554}
.pdf-open{color:#2563eb;font-weight:bold;font-size:14px;white-space:nowrap}
</style>
</head>
<body>
<header class="header">
<div class="logo">Ajay Chauhan</div>
<nav><a href="/index.html">Home</a><a href="/bcom-question-paper.html">Question Papers</a></nav>
</header>
<section class="hero"><h1>__YEAR__ Question Papers</h1><p>B.Com Semester __SEM__</p></section>
<section class="pdf-list">
__ROWS__
</section>
<footer><p>© 2026 Ajay Chauhan. All Rights Reserved.</p></footer>
</body>
</html>
"""

ROW = """<a class="pdf-row" href="__HREF__">
<span class="pdf-icon">📄</span>
<span class="pdf-name">__NAME__</span>
<span class="pdf-open">Open →</span>
</a>"""

for sem_folder, sem_no in SEMS.items():
    sem_path = os.path.join(BASE, sem_folder)
    if not os.path.isdir(sem_path):
        continue
    for year in sorted(os.listdir(sem_path)):
        ypath = os.path.join(sem_path, year)
        if not os.path.isdir(ypath):
            continue
        pdfs = sorted(
            [f for f in os.listdir(ypath) if f.lower().endswith(".pdf")],
            key=str.lower,
        )
        if not pdfs:
            continue
        rows = "\n".join(
            ROW.replace("__HREF__", quote(f))
               .replace("__NAME__", html.escape(f[:-4]))
            for f in pdfs
        )
        page = (TEMPLATE.replace("__SEM__", sem_no)
                        .replace("__YEAR__", year.replace("-", " "))
                        .replace("__ROWS__", rows))
        with open(os.path.join(ypath, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        print("Generated", ypath, len(pdfs), "files")
