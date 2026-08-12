#!/usr/bin/env bash
# Extract searchable plain text from raw/ into extracted/.
#   tools/extract.sh              extract sources that are new or changed
#   tools/extract.sh -f           re-extract everything
#   tools/extract.sh FILE...      extract specific files
set -euo pipefail

cd "$(dirname "$0")/.."

force=0
while getopts "fh" opt; do
  case $opt in
    f) force=1 ;;
    h) sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND - 1))

mkdir -p extracted

need() { command -v "$1" >/dev/null 2>&1; }

extract_one() {
  src=$1
  base=$(basename "$src")
  ext=$(printf '%s' "${base##*.}" | tr '[:upper:]' '[:lower:]')
  out="extracted/${base}.txt"
  tmp="${out}.part"

  # Already plain text — ripgrep reads raw/ directly, no copy needed.
  case $ext in
    md|markdown|txt|text|csv|json|yaml|yml) return 0 ;;
  esac

  if [ "$force" -eq 0 ] && [ -f "$out" ] && [ "$out" -nt "$src" ]; then
    return 0
  fi

  case $ext in
    pdf)
      need pdftotext || { printf 'skip  %s — needs: brew install poppler\n' "$base" >&2; return 0; }
      pdftotext -layout "$src" "$tmp"
      ;;
    doc|docx|odt|rtf|rtfd|html|htm|webarchive|wordml)
      if need textutil; then
        textutil -convert txt -stdout "$src" > "$tmp"
      elif need pandoc; then
        pandoc -t plain -o "$tmp" "$src"
      else
        printf 'skip  %s — needs: brew install pandoc\n' "$base" >&2; return 0
      fi
      ;;
    epub|tex|latex|rst|org|docbook)
      need pandoc || { printf 'skip  %s — needs: brew install pandoc\n' "$base" >&2; return 0; }
      pandoc -t plain -o "$tmp" "$src"
      ;;
    png|jpg|jpeg|tif|tiff)
      need tesseract || { printf 'skip  %s — needs: brew install tesseract\n' "$base" >&2; return 0; }
      tesseract "$src" "${tmp%.part}" >/dev/null 2>&1
      printf 'ocr   %s -> %s\n' "$base" "$out"
      return 0
      ;;
    *)
      printf 'skip  %s — no extractor for .%s\n' "$base" "$ext" >&2
      return 0
      ;;
  esac

  mv "$tmp" "$out"
  printf 'ok    %s -> %s (%s words)\n' "$base" "$out" "$(wc -w < "$out" | tr -d ' ')"
}

if [ $# -gt 0 ]; then
  for f in "$@"; do extract_one "$f"; done
else
  find raw -type f -not -path 'raw/assets/*' -not -name 'README.md' | sort | while IFS= read -r f; do
    extract_one "$f"
  done
fi
