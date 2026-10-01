#!/usr/bin/env python3
"""Generate Jay's Pizza theme music via VicSee Suno. Downloads all variations."""
import json, sys, time
import urllib.request, urllib.error, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = next(l.split("=", 1)[1].strip() for l in (Path.home() / ".hermes/.env").read_text().splitlines() if l.startswith("VICSEE_API_KEY="))
API = "https://vicsee.com/api/v1"

STYLE = ("Elegant modern Italian trattoria instrumental for a high-end wood-fired pizzeria. "
         "Warm fingerstyle acoustic guitar and mandolin lead melody over soft string quartet pads, "
         "gentle accordion swells, candlelit supperclub atmosphere. Subtle Indian fusion accents: "
         "distant sitar flourishes, soft tabla pulses, a low tanpura drone under the harmonies. "
         "Cinematic, refined, unhurried, romantic, 70 BPM. No vocals, no drums-heavy sections.")


def api(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}",
        data=json.dumps(body).encode() if body else None, method=method,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    body = {"model": "suno-v5-generate-music", "prompt": STYLE,
            "input": {"instrumental": True, "custom_mode": False}}
    try:
        resp = api("POST", "/generate", body)
    except urllib.error.HTTPError as e:
        print("submit failed:", e.read().decode()[:300]); sys.exit(2)
    data = resp.get("data", resp)
    tid = data.get("id")
    print("task:", tid, "| credits left:", data.get("creditsRemaining"), flush=True)
    for i in range(120):
        t = api("GET", f"/tasks/{tid}")
        d = t.get("data", t)
        status = d.get("status")
        print(f"[{i}] {status}", flush=True)
        if status == "completed":
            outdir = ROOT / "site/assets/music"
            outdir.mkdir(parents=True, exist_ok=True)
            res = d.get("result") or {}
            urls = []
            if isinstance(res, dict):
                if res.get("url"): urls.append(res["url"])
                for k in ("songs", "variations", "audio", "data"):
                    v = res.get(k)
                    if isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict) and item.get("url"): urls.append(item["url"])
                            elif isinstance(item, str): urls.append(item)
            print("URLs found:", len(urls), flush=True)
            for n, u in enumerate(urls, 1):
                dest = outdir / f"variation-{n}.mp3"
                subprocess.run(["curl", "-sL", "-m", "300", "-o", str(dest), u], check=True)
                print("SAVED", dest, dest.stat().st_size, flush=True)
            (outdir / "generation.json").write_text(json.dumps(d, indent=1, default=str))
            return
        if status in ("failed", "error"):
            print("FAILED:", json.dumps(d)[:400]); sys.exit(2)
        time.sleep(15)
    sys.exit("timeout")


if __name__ == "__main__":
    main()