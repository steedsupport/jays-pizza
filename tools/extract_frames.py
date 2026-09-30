#!/usr/bin/env python3
"""Extract scroll frames from the 4 masters and enforce Jay's Pizza quality budget.
Rules (locked by Varinder): 24fps cadence, desktop tier 1600w q90 <=1MB/frame,
mobile tier 900w <=600KB/frame. Output: assets/seq-N/ and assets/seq-N-m/."""
import subprocess, sys
from pathlib import Path
from PIL import Image
import io

ROOT = Path(__file__).resolve().parent.parent
VIDEOS = ROOT / "videos"
ASSETS = ROOT / "assets"
FPS = 24
TIERS = {"": (1600, 1_000_000, 90), "-m": (900, 600_000, 90)}  # suffix, max_width, max_bytes, q


def encode_budget(img: Image.Image, q: int, max_bytes: int) -> bytes:
    """Re-encode at q; if over budget walk quality down then width down."""
    w, h = img.size
    while q >= 60:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= max_bytes:
            return buf.getvalue()
        q -= 2
    # last resort: shrink width 8% and retry at q80
    while w > 600:
        w = int(w * 0.92)
        resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.LANCZOS)
        img2 = img.resize((w, int(img.height * w / img.width)), resample)
        buf = io.BytesIO()
        img2.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        if buf.tell() <= max_bytes:
            return buf.getvalue()
    raise RuntimeError("cannot fit budget")


def main():
    masters = sorted(VIDEOS.glob("*.mp4"))
    if not masters:
        sys.exit("no .mp4 masters in videos/")
    report = []
    for vid in masters:
        n = vid.stem.split("-")[-1]  # e.g. seq-1 -> 1
        for suffix, (width, max_bytes, q0) in TIERS.items():
            outdir = ASSETS / f"seq-{n}{suffix}"
            outdir.mkdir(parents=True, exist_ok=True)
            for old in outdir.glob("*.jpg"):
                old.unlink()
            raw = ROOT / f".tmp-frames{suffix}-{n}"
            raw.mkdir(exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid),
                            "-vf", f"fps={FPS},scale={width}:-2:flags=lanczos",
                            "-progress", "pipe:1", "-c:v", "mjpeg", "-q:v", "2",
                            str(raw / "%04d.jpg")], check=True)
            frames = sorted(raw.glob("*.jpg"))
            total = 0
            worst = 0
            for i, f in enumerate(frames, 1):
                img = Image.open(f).convert("RGB")
                data = encode_budget(img, q0, max_bytes)
                (outdir / f"seq{n}-{i:03d}.jpg").write_bytes(data)
                total += len(data)
                worst = max(worst, len(data))
                f.unlink()
            raw.rmdir()
            report.append(f"seq-{n}{suffix}: {len(frames)} frames, {total/1e6:.1f}MB total, "
                          f"worst frame {worst/1e3:.0f}KB (cap {max_bytes//1000}KB)")
            assert len(frames) in (240, 192, 168), f"unexpected frame count {len(frames)}"
    print("\n".join(report))


if __name__ == "__main__":
    main()