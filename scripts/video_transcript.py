"""Fetch a video's transcript as plain text with [m:ss] stamps, or rank videos by views.

Usage:
  python video_transcript.py <url> <out.txt> [--cookies FILE] [--ytdlp PATH] [--ffmpeg PATH] [--models DIR] [--ytdlp-opts "..."]
  python video_transcript.py --stats <url> [<url> ...] [--cookies FILE] [--ytdlp PATH] [--ytdlp-opts "..."]

Transcript order: the platform's subtitles first (YouTube captions; Bilibili CC/AI subtitles, which
need --cookies: a Netscape cookie file of a logged-in account), then speech recognition (faster-whisper large-v3 on
GPU, small on CPU). --stats prints views and favourites (Bilibili only; YouTube has no public
favourite count), sorted views first, then favourites.
Needs: pip install youtube-transcript-api faster-whisper yt-dlp; for GPU also
nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*".
"""
import argparse
import http.cookiejar
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


def youtube_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", s)
    return m.group(1) if m else (s if re.fullmatch(r"[\w-]{11}", s) else None)


def bvid(s):
    m = re.search(r"(BV[0-9A-Za-z]{10})", s)
    return m.group(1) if m else None


def stamp(sec, text):
    return f"[{int(sec) // 60}:{int(sec) % 60:02d}] {' '.join(text.split())}"


def parse_srt(srt):
    out = []
    for block in re.split(r"\n\s*\n", srt.strip()):
        rows = block.strip().splitlines()
        t = next((r for r in rows if "-->" in r), None)
        if not t:
            continue
        h, m, s = t.split("-->")[0].strip().replace(",", ".").split(":")
        text = " ".join(rows[rows.index(t) + 1:]).replace("<该字幕由算法自动生成>", "").strip()
        if text:
            out.append(stamp(int(h) * 3600 + int(m) * 60 + float(s), text))
    return out


def ytdlp(a, *args, **kw):
    return subprocess.run([a.ytdlp, "--ignore-config", "--no-playlist", *(["--cookies", a.cookies] if a.cookies else []),
                           *shlex.split(a.ytdlp_opts), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def youtube_captions(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        t = YouTubeTranscriptApi().fetch(vid, languages=["en", "zh-Hans", "zh", "zh-Hant"])
    except Exception:  # no captions, blocked IP, private video
        return []
    return [stamp(x.start, x.text) for x in t]


def platform_subtitles(url, a):
    with tempfile.TemporaryDirectory() as d:
        ytdlp(a, "--skip-download", "--write-subs", "--sub-langs", "all,-danmaku,-live_chat",
              "--sub-format", "srt/best", "-o", f"{d}/s.%(ext)s", url)
        f = next(Path(d).glob("*.srt"), None)
        return parse_srt(f.read_text(encoding="utf-8")) if f else []


def speech_to_text(url, a):
    import numpy as np
    import ctranslate2
    gpu = ctranslate2.get_cuda_device_count() > 0
    for p in ("nvidia.cublas", "nvidia.cudnn"):  # CUDA 12 DLLs shipped as pip wheels
        spec = importlib.util.find_spec(p) if gpu else None
        if not spec:
            gpu = False
            break
        d = os.path.join(list(spec.submodule_search_locations)[0], "bin")
        os.add_dll_directory(d)
        os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as d:
        r = ytdlp(a, "-f", "ba/b", "-o", f"{d}/a.%(ext)s", url)
        f = next(Path(d).glob("a.*"), None)
        if not f:
            sys.exit(f"{url}: audio download failed\n{r.stderr[-500:]}")
        # decode with ffmpeg, not PyAV: faster-whisper 1.2 + PyAV 19 is broken here
        pcm = subprocess.run([a.ffmpeg, "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                             capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    m = WhisperModel("large-v3" if gpu else "small", device="cuda" if gpu else "cpu",
                     compute_type="float16" if gpu else "int8", download_root=a.models)
    segs, _ = m.transcribe(x, vad_filter=True)
    return [stamp(s.start, s.text) for s in segs], "large-v3 GPU" if gpu else "small CPU"


def stats(url, a):
    b = bvid(url)
    if b:
        req = urllib.request.Request(f"https://api.bilibili.com/x/web-interface/view?bvid={b}",
                                     headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com/"})
        jar = http.cookiejar.MozillaCookieJar()
        if a.cookies:  # without buvid3/SESSDATA the API answers 412
            jar.load(a.cookies, ignore_discard=True, ignore_expires=True)
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        d = json.load(op.open(req, timeout=20))["data"]
        return d["stat"]["view"], d["stat"]["favorite"], d["title"]
    r = ytdlp(a, "-j", "--skip-download", url)
    d = json.loads(r.stdout or "{}")
    return d.get("view_count") or 0, None, d.get("title", f"? {r.stderr.strip()[-120:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("args", nargs="+")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--ytdlp", default="yt-dlp")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--models", help="where Whisper models are downloaded (default: Hugging Face cache)")
    ap.add_argument("--cookies", help="Netscape cookie file (Bilibili login: subtitles and --stats)")
    ap.add_argument("--ytdlp-opts", default="", help="extra yt-dlp options, e.g. --ffmpeg-location DIR --js-runtimes deno:PATH")
    a = ap.parse_args()

    if a.stats:
        rows = [(*stats(u, a), u) for u in a.args]
        for v, fav, title, u in sorted(rows, key=lambda r: (r[0], r[1] or 0), reverse=True):
            print(f"{v:>12,} views  {'-' if fav is None else f'{fav:,}':>9} favs  {title[:60]}  {u}")
        return

    url, out = a.args
    vid = youtube_id(url)
    lines, source = (youtube_captions(vid), "YouTube captions") if vid else ([], "")
    if not lines:
        lines, source = platform_subtitles(url, a), "platform subtitles"
    if not lines:
        lines, source = speech_to_text(url, a)
        source = f"speech recognition ({source})"
    Path(out).write_text("\n".join(lines), encoding="utf-8")
    print(f"{url}: {source}, {len(lines)} segments, last at {lines[-1].split(']')[0][1:]} -> {out}")


if __name__ == "__main__":
    assert youtube_id("https://www.youtube.com/watch?v=iEu2zQ7ZCTs&t=5") == "iEu2zQ7ZCTs"
    assert youtube_id("https://youtu.be/iEu2zQ7ZCTs") == "iEu2zQ7ZCTs"
    assert youtube_id("https://www.bilibili.com/video/BV1pu411o7BE") is None
    assert bvid("https://www.bilibili.com/video/BV1pu411o7BE?p=2") == "BV1pu411o7BE"
    assert parse_srt("1\n00:01:02,500 --> 00:01:04,000\n<该字幕由算法自动生成> 大家好\n\n2\n00:00:05,0 --> x\n") \
        == ["[1:02] 大家好"]
    main()
