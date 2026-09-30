#!/usr/bin/env python3
"""VicSee Veo 3.1 video generator for Jay's Pizza sections.
Usage: vicsee_generate.py <section 1-4> [--resume]
Anchors the video on keyframes/K<n>.png (base64 data URI), polls to completion,
downloads MP4 to videos/, records task state in videos/state.json for resume."""
import base64, json, sys, time
import urllib.request, urllib.error
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
KEYFILE = Path.home() / ".hermes/.env"
API = "https://vicsee.com/api/v1"

PROMPTS = {
    1: "Single continuous unbroken shot, zero camera cuts, one smooth constant-speed camera move, same kitchen and same lighting from first frame to last. Photoreal cinematic food-film grade, 24fps motion feel, native synchronized ambient sound. Slow steady camera push-in on strong pizzaiolo hands stretching a fresh Neapolitan dough round on the dark oak counter of a warm dawn brick pizzeria kitchen; flour dust drifts through the light beams; the dough visibly widens and breathes with each press and turn; the shot ends with the rested dough round glowing in warm rim light, ready for the peel. Audio: quiet dawn kitchen, soft dough taps on wood, flour whisper. No cuts, no jump cuts, no transitions, no text overlays.",
    2: "Single continuous unbroken shot, zero camera cuts, one smooth constant-speed camera move, same oven and same fire-light from first frame to last. Photoreal cinematic food-film grade, 24fps motion feel, native synchronized ambient sound. Slow lateral arc left-to-right at hearth level around the mouth of a blazing wood-fired brick oven dome; a long wooden peel glides in and lays a small margherita onto the stone oven floor; flames fold gently over the crust rim, leopard-spot char blooming; glowing embers swirl upward as the peel withdraws. Audio: deep fire crackle, stone hiss, wooden peel scrape. No cuts, no jump cuts, no transitions, no text overlays.",
    3: "Single continuous unbroken shot, zero camera cuts, one smooth constant-speed camera move on a locked overhead axis, same board and same soft light from first frame to last. Photoreal cinematic food-film grade, 24fps motion feel, native synchronized ambient sound. Slow overhead descend with gentle rightward drift over a dark oak board holding a just-baked leopard-spotted margherita, steam lifting; a hand enters frame and places fresh paneer cubes, then cilantro sprigs beside torn basil; a slow spiral of glossy saffron-tomato chutney drizzles across the melting cheese, glistening. Audio: crisp crust tick, soft sizzle, copper cup set down. No cuts, no jump cuts, no transitions, no text overlays.",
    4: "Single continuous unbroken shot, zero camera cuts, one smooth constant-speed camera move, same table and same candlelight from first frame to last. Photoreal cinematic food-film grade, 24fps motion feel, native synchronized ambient sound. Pure slow dolly pull-back from close on the finished paneer-and-basil fusion pizza on its rustic wooden board; steam curls off the pie; candles, glassware and exposed brick of a cozy trattoria resolve into warm evening glow; the camera settles centered above the board with the small red-lettered JAY'S PIZZA menu card clearly legible, symmetric hero composition. Audio: warm room ambience, candle flicker, one distant contented laugh. No cuts, no jump cuts, no transitions, no text overlays.",
}

KEY = next(l.split("=", 1)[1].strip() for l in KEYFILE.read_text().splitlines()
           if l.startswith("VICSEE_API_KEY="))


def api(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        f"{API}{path}", method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def upload_anchor(path: Path) -> str:
    """Presign -> PUT to R2 -> return public URL (per VicSee MCP client flow)."""
    data = path.read_bytes()
    sign = api("POST", "/upload", {"contentType": "image/jpeg",
                                   "sizeBytes": len(data)})["data"]
    req = urllib.request.Request(sign["uploadUrl"], data=data, method="PUT",
                                 headers={"Content-Type": "image/jpeg"})
    with urllib.request.urlopen(req, timeout=120) as r:
        assert r.status in (200, 201)
    return sign["publicUrl"]


def ensure_anchor_url(n: int, state: dict, state_file: Path) -> str:
    sec = state.setdefault(str(n), {})
    if "anchor_url" not in sec:
        sec["anchor_url"] = upload_anchor(ROOT / f"videos/anchor-{n}.jpg")
        state_file.write_text(json.dumps(state))
    return sec["anchor_url"]


def download(url: str, dest: Path):
    import subprocess
    subprocess.run(["curl", "-sL", "-m", "300", "-o", str(dest), url], check=True)


def main():
    n = int(sys.argv[1])
    resume = "--resume" in sys.argv
    state_file = ROOT / "videos/state.json"
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    sec = state.get(str(n), {})

    if not resume or "task_id" not in sec:
        anchor = ensure_anchor_url(n, state, state_file)
        body = {"model": "veo-3-1-image-to-video",
                "prompt": PROMPTS[n],
                "input": {"image_urls": [anchor],
                          "duration": 10, "resolution": "720p", "aspect_ratio": "16:9",
                          "audio": True}}
        try:
            resp = api("POST", "/generate", body)
        except urllib.error.HTTPError as e:
            err = e.read().decode()[:300]
            print("duration=10 rejected:", err)
            body["input"]["duration"] = 8
            resp = api("POST", "/generate", body)
        rdata = resp.get("data", resp)
        if not rdata.get("id", resp.get("id", "")):
            print("SUBMIT FAILED:", json.dumps(resp)[:300])
            sys.exit(2)
        sec["task_id"] = rdata.get("id", resp.get("id", ""))
        sec["submitted"], sec["task"] = True, rdata
        state[str(n)] = sec
        state_file.parent.mkdir(exist_ok=True)
        state_file.write_text(json.dumps(state))

    tid = sec["task_id"]
    print(f"section {n} task {tid} — polling")
    for i in range(180):
        t = api("GET", f"/tasks/{tid}")
        data = t.get("data", t)
        status = data.get("status", "?")
        print(f"  [{i}] {status}", flush=True)
        if status == "completed":
            url = (data.get("result") or data).get("url") or data.get("video_url") or data.get("output", {}).get("url")
            dest = ROOT / f"videos/seq-{n}.mp4"
            download(url, dest)
            sec["done"], sec["url"] = True, url
            state[str(n)] = sec
            state_file.write_text(json.dumps(state))
            print("SAVED", dest, dest.stat().st_size, "bytes")
            return
        if status in ("failed", "error"):
            print("FAILED:", json.dumps(data)[:400])
            state[str(n)] = {"last_failed_task": tid}
            state_file.write_text(json.dumps(state))
            sys.exit(2)
        time.sleep(15)
    sys.exit("timeout")


if __name__ == "__main__":
    main()