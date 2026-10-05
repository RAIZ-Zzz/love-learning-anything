"""Fetch a YouTube video's captions as plain text with [m:ss] stamps.

Usage: python video_transcript.py <url-or-id> <out.txt> [--lang en zh-Hans ...]
Needs: pip install youtube-transcript-api (no API key).
"""
import argparse
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi

# ponytail: YouTube captions only; add a yt-dlp subtitle fallback when a Bilibili or caption-less video is needed


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", s)
    return m.group(1) if m else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--lang", nargs="+", default=["en", "zh-Hans", "zh", "zh-Hant"])
    a = ap.parse_args()
    vid = video_id(a.video)
    try:
        t = YouTubeTranscriptApi().fetch(vid, languages=a.lang)
    except Exception as e:  # no captions, blocked IP, private video
        sys.exit(f"{vid}: no transcript ({type(e).__name__}); pick another video")
    lines = [f"[{int(x.start) // 60}:{int(x.start) % 60:02d}] {' '.join(x.text.split())}" for x in t]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{vid}: {len(lines)} segments, {int(t[-1].start) // 60} min, {sum(len(l.split()) for l in lines)} words -> {a.out}")


if __name__ == "__main__":
    assert video_id("https://www.youtube.com/watch?v=iEu2zQ7ZCTs&t=5") == "iEu2zQ7ZCTs"
    assert video_id("https://youtu.be/iEu2zQ7ZCTs") == "iEu2zQ7ZCTs"
    assert video_id("iEu2zQ7ZCTs") == "iEu2zQ7ZCTs"
    main()
