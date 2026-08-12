#!/usr/bin/env bash
# Search the wiki, writing, and sources (including extracted PDF/doc text).
#   tools/wiki-search.sh "query"        search wiki/ (default)
#   tools/wiki-search.sh -w "query"     search wiki/ and writing/
#   tools/wiki-search.sh -s "query"     search sources: raw/ and extracted/
#   tools/wiki-search.sh -a "query"     search everything
#   tools/wiki-search.sh -t "query"     titles/filenames only
set -euo pipefail

cd "$(dirname "$0")/.."

dirs=(wiki)
mode=text
glob='*.md'

while getopts "awsth" opt; do
  case $opt in
    a) dirs=(wiki writing raw extracted); glob='*' ;;
    w) dirs=(wiki writing) ;;
    s) dirs=(raw extracted); glob='*' ;;
    t) mode=title ;;
    h) sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND - 1))

[ $# -ge 1 ] || { echo "usage: wiki-search.sh [-w|-s|-a] [-t] <query>" >&2; exit 1; }
query="$*"

# Only search directories that exist — writing/ or extracted/ may not yet.
present=()
for d in "${dirs[@]}"; do [ -d "$d" ] && present+=("$d"); done
[ ${#present[@]} -gt 0 ] || { echo "no matches"; exit 0; }

if command -v rg >/dev/null 2>&1; then
  if [ "$mode" = title ]; then
    rg --files "${present[@]}" -g "$glob" | rg -i -- "$query" || echo "no matches"
  else
    rg -i --heading --line-number --color always -C 2 -g "$glob" -- "$query" "${present[@]}" || echo "no matches"
  fi
else
  if [ "$mode" = title ]; then
    find "${present[@]}" -name "$glob" | grep -i -- "$query" || echo "no matches"
  else
    grep -rin -C 2 --include="$glob" -- "$query" "${present[@]}" || echo "no matches"
  fi
fi
