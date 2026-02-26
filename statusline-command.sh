#!/usr/bin/env bash
# Claude Code status line — clean unicode aesthetic
# Input: JSON via stdin

input=$(cat)

SEP="  "   # thin double-space separator (visually quiet)
DOT=" · "  # mid-dot for within-group separation

# --- Parse JSON fields ---
cwd=$(echo "$input"   | jq -r '.workspace.current_dir // .cwd // "?"')
model=$(echo "$input" | jq -r '.model.display_name // "?"')
remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')

# --- Directory: shorten home to ~ ---
dir="${cwd/#$HOME/~}"

# --- Git context (best-effort, no lock contention) ---
git_info=""
if git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null \
           || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)

  git_status=$(git -C "$cwd" status --porcelain 2>/dev/null)

  # Compact flag string: each symbol only appears if relevant
  flags=""
  echo "$git_status" | grep -q "^A\|^M " && flags="${flags}●"   # staged
  echo "$git_status" | grep -q "^ M\|^M" && flags="${flags}○"   # modified
  echo "$git_status" | grep -q "^??"     && flags="${flags}…"   # untracked

  ahead=$(git  -C "$cwd" rev-list --count "@{u}..HEAD" 2>/dev/null || true)
  behind=$(git -C "$cwd" rev-list --count "HEAD..@{u}" 2>/dev/null || true)
  ab=""
  [ -n "$ahead"  ] && [ "$ahead"  -gt 0 ] 2>/dev/null && ab="${ab}↑${ahead}"
  [ -n "$behind" ] && [ "$behind" -gt 0 ] 2>/dev/null && ab="${ab}↓${behind}"

  git_part="⎇ ${branch}"
  [ -n "$flags" ] && git_part="${git_part}${DOT}${flags}"
  [ -n "$ab"    ] && git_part="${git_part} ${ab}"
  git_info="${SEP}${git_part}"
fi

# --- Model (strip "Claude " prefix to save space) ---
model_short="${model#Claude }"
model_info="${SEP}◆ ${model_short}"

# --- Context: mini progress bar + percentage ---
ctx_info=""
if [ -n "$remaining" ]; then
  used=$((100 - remaining))
  # 8-segment bar: filled ▓, empty ░
  filled=$(( used * 8 / 100 ))
  bar=""
  for i in $(seq 1 8); do
    if [ "$i" -le "$filled" ]; then
      bar="${bar}▓"
    else
      bar="${bar}░"
    fi
  done
  ctx_info="${SEP}${bar} ${remaining}%"
fi

# --- Compose ---
printf '%s%s%s%s' "${dir}" "${git_info}" "${model_info}" "${ctx_info}"
