#!/usr/bin/env sh
# play.sh - play a baked braille_life.txt (frames separated by @@FRAME@@)
# Usage: ./play.sh [file] [frame_delay_seconds]
# Defaults: file=braille_life.txt  delay=0.06

FILE=${1:-braille_life.txt}
DELAY=${2:-0.06}        # seconds between frames for gawk/python player
PV_RATE=${PV_RATE:-1200} # bytes/sec for pv fallback
RS="@@FRAME@@\n"

# restore cursor and normal buffer
_cleanup() {
  # show cursor, leave alt buffer
  printf '\033[?25h' 2>/dev/null || true
  printf '\033[?1049l' 2>/dev/null || true
}
# ensure cleanup on exit / signals
trap '_cleanup' EXIT INT TERM

# sanity checks
if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE" >&2
  exit 2
fi

# enter alternate buffer + hide cursor
printf '\033[?1049h'   # switch to alternate screen buffer
printf '\033[?25l'     # hide cursor

# prefer gawk (supports multi-char RS), then python3, then pv
if command -v gawk >/dev/null 2>&1; then
  # Use gawk: split by RS and sleep between frames
  # NR>1 because if file starts with delimiter we avoid an empty frame
  gawk -v RS="$RS" -v delay="$DELAY" 'NR>1{ printf "%s", $0; fflush(); system("sleep " delay) }' "$FILE"
  exit 0
fi

if command -v python3 >/dev/null 2>&1; then
  python3 - "$FILE" "$DELAY" <<'PY' || true
import sys, time
file = sys.argv[1]
delay = float(sys.argv[2])
delim = "@@FRAME@@\n"
# Read entire file then split — simple and portable. If file is huge,
# this can be changed to a streaming parser.
with open(file, "r", encoding="utf-8") as f:
    data = f.read()
frames = data.split(delim)
# If first split is empty (file started with delim), skip it
for i, frame in enumerate(frames):
    if i==0 and not frame:
        continue
    sys.stdout.write(frame)
    sys.stdout.flush()
    time.sleep(delay)
PY
  exit 0
fi

# pv fallback: rate-limited raw output; strip delimiter with sed
if command -v pv >/dev/null 2>&1; then
  pv -qL "$PV_RATE" "$FILE" | sed '/@@FRAME@@/d'
  exit 0
fi

# last resort: brute cat (will likely just show final frame)
cat "$FILE"
exit 0
