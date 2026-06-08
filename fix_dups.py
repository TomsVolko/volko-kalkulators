import re

path = r"C:\Users\matri\OneDrive - VolkoEngineering\volko-kalkulators\index.html"

with open(path, encoding="utf-8") as f:
    html = f.read()

# 1. Remove duplicate const SVC_BASE block from ar_js section
# (the one that uses bk_small/bk_mid/bk_large)
html = re.sub(
    r"\nconst SVC_BASE = \{\n    esi:950, taa:400, nod:950, bk_small:1400, bk_mid:2000, bk_large:3000,\n    ti:400, eps:370, elt:350, dv:350,\n\};",
    "",
    html
)

# 2. Fix RECS priceFn references from bk_small/mid/large to bk_s/m/l
html = html.replace("SVC_BASE.bk_small", "SVC_BASE.bk_s")
html = html.replace("SVC_BASE.bk_mid", "SVC_BASE.bk_m")
html = html.replace("SVC_BASE.bk_large", "SVC_BASE.bk_l")

# 3. Remove duplicate function declarations (keeping AR_JS_MAIN versions)
# r50 duplicate (the one from ar_js - it's "function r50(n) { return Math.round(n / 50) * 50; }")
html = re.sub(
    r"\nfunction r50\(n\) \{ return Math\.round\(n / 50\) \* 50; \}",
    "", html, count=1  # remove only second occurrence
)
# r50c - only in ar_js, rename references to use r50 (same function)
html = re.sub(
    r"\nfunction r50c\(n\) \{ return Math\.round\(n / 50\) \* 50; \}",
    "", html
)
# Replace r50c calls with r50
html = html.replace("r50c(", "r50(")

# 4. Remove duplicate eur function
html = re.sub(
    r"\nfunction eur\(n\) \{ return n\.toLocaleString\('lv-LV'\) \+ ' EUR'; \}",
    "", html, count=1
)

# 5. Remove duplicate isLegal function
html = re.sub(
    r"\nfunction isLegal\(t\) \{ return \['la','lbv','lbp','lc'\]\.includes\(t\); \}",
    "", html, count=1
)

# 6. Remove duplicate GC declaration
html = re.sub(
    r"\nconst GC = \{ I:0\.75, II:1\.20, III:1\.80 \};",
    "", html, count=1
)

# 7. Remove duplicate grp function
html = re.sub(
    r"\nfunction grp\(a,f\)\{ if\(a<=25&&f<=1\)return'I'; if\(a>1500\|\|f>=4\)return'III'; return'II'; \}",
    "", html, count=1
)

# 8. Remove duplicate bi function (the one using BRACKS, not AR_BRACKS)
html = re.sub(
    r"\nfunction bi\(a\)\{ for\(let i=0;i<BRACKS\.length;i\+\+\)if\(a<=BRACKS\[i\]\)return i; return BRACKS\.length-1; \}",
    "", html, count=1
)

# 9. Rename renderARSection to renderARPanels (to match calls in calcAR)
html = html.replace("function renderARSection(", "function renderARPanels(")
# Keep the call-site name consistent (calcAR already calls renderARPanels)

# Verify no more duplicates
import sys
scriptStart = html.find("<script>") + 8
scriptEnd = html.rfind("</script>")
js = html[scriptStart:scriptEnd]

lines = js.split("\n")
decls = {}
dups = []
for i, line in enumerate(lines):
    m = re.match(r"^(const|let|var|function)\s+([a-zA-Z_\$][a-zA-Z0-9_\$]*)", line)
    if m:
        name = m.group(2)
        if name in decls:
            dups.append(f"DUP: {name} at line {i+1} (first at {decls[name]})")
        else:
            decls[name] = i + 1

if dups:
    print("REMAINING DUPLICATES:")
    for d in dups: print(d)
else:
    print("NO DUPLICATES — clean!")

# Write fixed file
with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Fixed file written: {len(html)} chars")
