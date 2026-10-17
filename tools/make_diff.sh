#!/bin/bash
# Build revision_diff.pdf: submitted paper (BASE) vs latest paper, marked with latexdiff.
# Usage: tools/make_diff.sh <paper-git-dir> <output-pdf>
set -e
PAPER=$(realpath "$1"); OUT=$(realpath -m "$2")
BASE=${BASE:-4d6184a}                      # submitted version (26-4628 v1)
LATEXDIFF=${LATEXDIFF:-latexdiff}
W=$(mktemp -d)
git -C "$PAPER" archive "$BASE" | (mkdir -p "$W/old" && tar -x -C "$W/old")
git -C "$PAPER" archive HEAD  | (mkdir -p "$W/new" && tar -x -C "$W/new")
cd "$W/new"
$LATEXDIFF --type=CFONT --math-markup=whole --flatten "$W/old/main.tex" main.tex > diff.tex 2> ld.log
# keep the combined response under 2 MB: shrink large raster figures
python3 - <<'PY'
import glob, os
from PIL import Image
for f in glob.glob('Figures/**/*.png', recursive=True):
    if os.path.getsize(f) > 100000:
        im = Image.open(f).convert('RGB'); im.thumbnail((1000, 1000))
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(f, optimize=True)
PY
pdflatex -interaction=nonstopmode diff.tex >/dev/null || true
bibtex diff >/dev/null || true
pdflatex -interaction=nonstopmode diff.tex >/dev/null || true
pdflatex -interaction=nonstopmode diff.tex >/dev/null || true
test -s diff.pdf
cp diff.pdf "$OUT"
echo "revision diff: $(git -C "$PAPER" rev-parse --short HEAD) vs $BASE -> $OUT ($(stat -c %s "$OUT") bytes)"
