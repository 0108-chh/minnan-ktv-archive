#!/usr/bin/env python3
"""Download a batch of Minnan MVs from Bilibili and upload them to the GitHub Release.

Logic:
- mvs/mv_list.json holds all MV items (bvid + title).
- Files already attached to the Release `mv-archive` are considered done.
- Each run downloads the next BATCH_SIZE missing MVs and uploads them.
- Failed items are simply retried on the next run.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

BATCH = int(os.environ.get("BATCH_SIZE", "30"))
COOKIE = os.environ.get("BILI_COOKIE", "").strip()
TAG = "mv-archive"
DL = Path("downloads")
DL.mkdir(exist_ok=True)


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True)


def sanitize(title: str) -> str:
    t = re.sub(r'[\\/:*?"<>|\r\n\t]', " ", title)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:100]


if COOKIE:
    # Netscape-format cookie file carrying SESSDATA for higher-quality streams
    Path(".cookies.txt").write_text(
        ".bilibili.com\tTRUE\t/\tTRUE\t0\tSESSDATA\t" + COOKIE + "\n",
        encoding="utf-8",
    )

items = json.loads(Path("mvs/mv_list.json").read_text(encoding="utf-8"))

r = gh("release", "view", TAG, "--json", "assets", "-q", ".assets[].name")
if r.returncode != 0:
    done_names = []
else:
    done_names = [l.strip() for l in r.stdout.splitlines() if l.strip()]

done_bvids = {n.rsplit("_", 1)[-1][:-4] for n in done_names if n.endswith(".mp4")}
print(f"already uploaded: {len(done_bvids)} MVs")

batch = []
for it in items:
    if len(batch) >= BATCH:
        break
    if it["bvid"] in done_bvids:
        continue
    batch.append((it, f"{sanitize(it['title'])}_{it['bvid']}.mp4"))

print(f"to download this run: {len(batch)}")
if not batch:
    print("ALL DONE: every MV in the list has been uploaded.")
    sys.exit(0)

ok_files = []
failed = []
for it, name in batch:
    bvid = it["bvid"]
    url = f"https://www.bilibili.com/video/{bvid}"
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f",
        "bv*[height<=1080]+ba/b",
        "--merge-output-format",
        "mp4",
        "--retries",
        "3",
        "--no-progress",
        "-o",
        str(DL / f"{bvid}.%(ext)s"),
    ]
    if COOKIE:
        cmd += ["--cookies", ".cookies.txt"]
    cmd.append(url)

    print(f"==> [{len(ok_files)+len(failed)+1}/{len(batch)}] {name}", flush=True)
    subprocess.run(cmd)
    f = DL / f"{bvid}.mp4"
    if f.exists() and f.stat().st_size > 1_000_000:
        target = DL / name
        f.rename(target)
        ok_files.append(target)
    else:
        failed.append(bvid)
        print(f"FAILED: {bvid}", flush=True)
    # clean up leftovers from failed merges (e.g. .part files)
    for p in DL.glob(f"{bvid}.*"):
        p.unlink(missing_ok=True)
    time.sleep(3)

if ok_files:
    r = gh("release", "view", TAG)
    if r.returncode != 0:
        rc = gh(
            "release",
            "create",
            TAG,
            "--title",
            "闽南语经典歌曲MV存档",
            "--notes",
            "B站UP主 jmhbee 合集《经典闽南语歌曲合集》中的MV存档（私人备份）",
        )
        if rc.returncode != 0:
            print("create release failed:", rc.stderr[:500])
    for f in ok_files:
        for attempt in range(3):
            r = gh("release", "upload", TAG, str(f), "--clobber")
            if r.returncode == 0:
                break
            print(f"upload retry {attempt}: {r.stderr[:300]}", flush=True)
            time.sleep(10)

print(f"uploaded: {len(ok_files)} | failed this run: {len(failed)} {failed}")
if failed:
    # not fatal: remaining items are picked up by the next run
    sys.exit(0)
