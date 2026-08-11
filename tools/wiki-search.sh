#!/usr/bin/env bash
# Search the wiki and raw sources.
#   tools/wiki-search.sh "query"        search wiki/ (default)
#   tools/wiki-search.sh -a "query"     search wiki/ and raw/
#   tools/wiki-search.sh -t "query"     titles/filenames only
set -euo pipefail

cd "$(dirname "$0")/.."

dirs=(wiki)
mode=text

while getopts "ath" opt; do
  case $opt in
    a) dirs=(wiki raw) ;;
    t) mode=title ;;
    h) sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND - 1))

[ $# -ge 1 ] || { echo "usage: wiki-search.sh [-a] [-t] <query>" >&2; exit 1; }
query="$*"

if command -v rg >/dev/null 2>&1; then
  if [ "$mode" = title ]; then
    rg --files "${dirs[@]}" -g '*.md' | rg -i -- "$query" || echo "no matches"
  else
    rg -i --heading --line-number --color always -C 2 -g '*.md' -- "$query" "${dirs[@]}" || echo "no matches"
  fi
else
  if [ "$mode" = title ]; then
    find "${dirs[@]}" -name '*.md' | grep -i -- "$query" || echo "no matches"
  else
    grep -rin -C 2 --include='*.md' -- "$query" "${dirs[@]}" || echo "no matches"
  fi
fi
