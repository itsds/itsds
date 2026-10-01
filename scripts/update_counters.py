"""Refresh the Profile Views / Followers / Stars pills in assets/ from live numbers.
Run by .github/workflows/counters.yml on a schedule."""
import json, os, re, urllib.request

USER = os.environ.get("PROFILE_USER", "itsds")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "profile-counters"})
    if TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def fmt(n):
    if n >= 10000:
        return f"{n / 1000:.0f}k"
    if n >= 1000:
        return f"{n / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)


def followers():
    return json.loads(get(f"https://api.github.com/users/{USER}"))["followers"]


def stars():
    total, page = 0, 1
    while True:
        repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}"))
        total += sum(r.get("stargazers_count", 0) for r in repos)
        if len(repos) < 100:
            return total
        page += 1


def views():
    # The view counter only serves a badge image; read the number off it.
    svg = get(f"https://komarev.com/ghpvc/?username={USER}", accept="image/svg+xml")
    nums = re.findall(r">\s*([\d,]+)\s*<", svg)
    return int(nums[-1].replace(",", ""))


def write(name, value):
    tpl = open(os.path.join(ROOT, "assets", "templates", f"counter-{name}.svg"), encoding="utf-8").read()
    out = os.path.join(ROOT, "assets", f"counter-{name}.svg")
    open(out, "w", encoding="utf-8").write(tpl.replace("__COUNT__", value))
    print(f"{name}: {value}")


for name, fn in [("views", views), ("followers", followers), ("stars", stars)]:
    try:
        write(name, fmt(fn()))
    except Exception as e:  # keep the last good pill if a source is down
        print(f"{name}: skipped ({e})")
        if not os.path.exists(os.path.join(ROOT, "assets", f"counter-{name}.svg")):
            write(name, "—")
