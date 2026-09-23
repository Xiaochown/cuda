#!/usr/bin/env bash
# Secret scan + public access verification for Xiaochown/cuda
cd /root/cuda-ai || exit 1

echo "=== SECRET SCAN (harus kosong) ==="
grep -rInE 'sk-[A-Za-z0-9_-]{12,}|gsk-|fc-[a-f0-9]{20,}|ghp_|gho_|ghs_|AIza[0-9A-Za-z_-]{20,}' \
  --include='*.md' --include='*.py' --include='*.html' --include='*.json' --include='*.csv' . 2>/dev/null | head -10
echo "(scan selesai)"

echo
echo "=== RAW PUBLIC ACCESS (tanpa auth) ==="
for f in README.md PROMPT.md AGENT_BRIEF.md TASKS.md PLAN.md docs/DECISIONS.md docs/SETUP_LAPTOP.md docs/ANSWERS.md; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 20 "https://raw.githubusercontent.com/Xiaochown/cuda/master/$f")
  printf "%-26s %s\n" "$f" "$code"
done

echo
echo "=== repo page ==="
curl -s -o /dev/null -w 'github.com/Xiaochown/cuda: %{http_code}\n' -m 20 https://github.com/Xiaochown/cuda
