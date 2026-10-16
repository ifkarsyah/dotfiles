#!/usr/bin/env bash
# Build a contact sheet (grid of frames) from a rendered video for review.
# Usage: tools/contact_sheet.sh <video.mp4> <out.png> [seconds_between_frames] [columns]
set -euo pipefail
video="$1"; out="$2"; every="${3:-4}"; cols="${4:-4}"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video")
n=$(python3 -c "import math;print(max(1, math.ceil($dur/$every)))")
rows=$(python3 -c "import math;print(math.ceil($n/$cols))")
ffmpeg -v error -y -i "$video" \
  -vf "fps=1/$every,scale=640:-1,drawtext=text='%{pts\:hms}':x=8:y=8:fontcolor=white:fontsize=16:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=4:color=gray" \
  -frames:v 1 "$out"
echo "$out  (duration ${dur}s, $n frames)"
