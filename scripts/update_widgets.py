"""Generate the Contribution Activity graph and GitHub Trophies cards as SVGs in assets/.

Replaces the hosted github-readme-activity-graph / github-profile-trophy services, whose
public instances now answer 402 (deployment disabled). Run by .github/workflows/counters.yml.

    python scripts/update_widgets.py            # live data (needs GH_TOKEN)
    python scripts/update_widgets.py --mock f   # render from a saved JSON response
    python scripts/update_widgets.py --seed     # placeholder cards before the first run
"""
import base64, datetime as dt, json, math, os, sys, urllib.request
from html import escape

USER = os.environ.get("PROFILE_USER", "itsds")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
W, PAD = 880, 16                      # same canvas and gutter as the section images
CARD_W = W - 2 * PAD

# ---------- palettes: sky/violet (DS_GitHub_Profile.html) and Ember & Parchment ----------
PALETTES = {
    "": {
        "dark": dict(card="#171d30", border="rgba(255,255,255,0.06)", fg="#e2e8f0", muted="#8892a8", dim="#5a6478",
                     grid="rgba(255,255,255,0.06)", a1="#38bdf8", a2="#a78bfa", a3="#f472b6", heading="#f1f5f9"),
        "light": dict(card="#ffffff", border="rgba(0,0,0,0.08)", fg="#1e293b", muted="#64748b", dim="#94a3b8",
                      grid="rgba(0,0,0,0.06)", a1="#0284c7", a2="#7c3aed", a3="#db2777", heading="#0f172a"),
    },
    "ember-": {
        "dark": dict(card="#1e1b16", border="#332e24", fg="#e9e1d1", muted="#a89b86", dim="#75695a",
                     grid="rgba(255,248,235,0.06)", a1="#f0773a", a2="#d4a72c", a3="#3fb68b", heading="#f6efe1"),
        "light": dict(card="#ffffff", border="#e4ddcb", fg="#2b2418", muted="#6b5f4d", dim="#978a74",
                      grid="rgba(60,40,15,0.07)", a1="#c2410c", a2="#b8860b", a3="#0f6f5c", heading="#1c160e"),
    },
}


def font_css():
    out = []
    for fam, wt, f in [("Space Grotesk", 500, "space-grotesk-500"), ("Space Grotesk", 700, "space-grotesk-700"),
                       ("IBM Plex Mono", 500, "ibm-plex-mono-500")]:
        b64 = base64.b64encode(open(os.path.join(ROOT, "scripts", "fonts", f + ".woff2"), "rb").read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(out)


FONTS = None
SANS = "'Space Grotesk','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'IBM Plex Mono',SFMono-Regular,Consolas,monospace"


def svg_doc(h, title, body, defs=""):
    global FONTS
    FONTS = FONTS or font_css()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" '
            f'aria-label="{escape(title)}"><title>{escape(title)}</title><defs><style>{FONTS}</style>{defs}</defs>{body}</svg>')


# ---------- data ----------
QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, isFork: false) { totalCount nodes { stargazerCount } }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                                          "User-Agent": "profile-widgets"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]


# ---------- contribution activity (last 31 days) ----------
def nice_max(v):
    """Top of the y-axis: four equal, whole-number steps that clear the peak."""
    raw = max(v, 1) / 4
    mag = 10 ** math.floor(math.log10(raw)) if raw >= 1 else 1
    for m in (1, 2, 2.5, 3, 4, 5, 6, 8, 10):
        step = m * mag
        if step >= raw and (step * 4) == int(step * 4) and step == int(step):
            return int(step * 4)
    return int(math.ceil(raw)) * 4


def activity_svg(days, total_year, p, title_suffix):
    days = days[-31:]
    counts = [d["contributionCount"] for d in days]
    h = 300
    top_pad, bottom_pad, left_pad, right_pad = 74, 44, 52, 24
    x0, x1 = PAD + left_pad, PAD + CARD_W - right_pad
    y0, y1 = top_pad, h - bottom_pad                      # y0 top of plot, y1 baseline
    ymax = nice_max(max(counts) if counts else 0)
    n = max(len(counts) - 1, 1)
    xs = [x0 + i * (x1 - x0) / n for i in range(len(counts))]
    ys = [y1 - (c / ymax) * (y1 - y0) for c in counts]
    last31 = sum(counts)

    # smooth path (Catmull-Rom → cubic Bézier), clamped to the plot
    def smooth(pts):
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(len(pts) - 1):
            p0 = pts[i - 1] if i else pts[i]
            p1, p2 = pts[i], pts[i + 1]
            p3 = pts[i + 2] if i + 2 < len(pts) else p2
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, min(y1, max(y0, p1[1] + (p2[1] - p0[1]) / 6)))
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, min(y1, max(y0, p2[1] - (p3[1] - p1[1]) / 6)))
            d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return d

    pts = list(zip(xs, ys))
    line = smooth(pts) if pts else ""
    area = f"{line} L{xs[-1]:.1f},{y1} L{xs[0]:.1f},{y1} Z" if pts else ""

    grid, ylabels = [], []
    for i in range(5):
        v = ymax * i / 4
        y = y1 - (v / ymax) * (y1 - y0)
        grid.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{p["grid"]}" stroke-width="1"/>')
        lab = f"{v:g}" if v != int(v) else str(int(v))
        ylabels.append(f'<text x="{x0 - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{p["dim"]}">{lab}</text>')
    xlabels = []
    for i, d in enumerate(days):
        if i % 5 == 0 or i == len(days) - 1:
            day = dt.date.fromisoformat(d["date"])
            xlabels.append(f'<text x="{xs[i]:.1f}" y="{y1 + 22}" text-anchor="middle" font-family="{MONO}" font-size="11" '
                           f'fill="{p["dim"]}">{day.strftime("%d %b")}</text>')
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{p["card"]}" stroke="{p["a3"]}" stroke-width="2"/>'
                   for x, y in pts)
    peak_i = max(range(len(counts)), key=lambda i: counts[i]) if counts else 0

    defs = (f'<linearGradient id="ln" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{p["a1"]}"/>'
            f'<stop offset=".5" stop-color="{p["a2"]}"/><stop offset="1" stop-color="{p["a3"]}"/></linearGradient>'
            f'<linearGradient id="ar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{p["a2"]}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{p["a2"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{p["a1"]}"/><stop offset=".5" stop-color="{p["a2"]}"/>'
            f'<stop offset="1" stop-color="{p["a3"]}"/></linearGradient>'
            f'<clipPath id="cc"><rect x="{PAD}" y="1" width="{CARD_W}" height="{h - 2}" rx="12"/></clipPath>')
    peak = ""
    if counts and counts[peak_i] > 0:
        px, py = xs[peak_i], ys[peak_i]
        peak = (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{p["a3"]}"/>'
                f'<text x="{px:.1f}" y="{py - 12:.1f}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="500" '
                f'fill="{p["fg"]}">{counts[peak_i]}</text>')
    body = (f'<rect x="{PAD + .5}" y="1.5" width="{CARD_W - 1}" height="{h - 3}" rx="12" fill="{p["card"]}" stroke="{p["border"]}"/>'
            f'<g clip-path="url(#cc)"><rect x="{PAD}" y="1" width="{CARD_W}" height="3" fill="url(#bar)"/></g>'
            f'<text x="{PAD + 24}" y="38" font-family="{SANS}" font-size="15" font-weight="700" fill="{p["heading"]}">Last 31 days</text>'
            f'<text x="{PAD + 24}" y="57" font-family="{SANS}" font-size="12.5" font-weight="500" fill="{p["muted"]}">'
            f'{last31} contributions · {total_year} in the past year{title_suffix}</text>'
            + "".join(grid) + "".join(ylabels) + "".join(xlabels) +
            (f'<path d="{area}" fill="url(#ar)"/><path d="{line}" fill="none" stroke="url(#ln)" stroke-width="2.5" '
             f'stroke-linecap="round" stroke-linejoin="round"/>' if pts else "") + dots + peak)
    return svg_doc(h, f"Contribution activity: {last31} contributions in the last 31 days", body, defs)


# ---------- trophies ----------
RANKS = [("S", 3), ("A", 2), ("B", 1), ("C", 0)]


def rank(value, thresholds):
    # thresholds = [C, B, A, S]
    for letter, idx in RANKS:
        if value >= thresholds[idx]:
            return letter
    return "?"


def trophy_cards(u):
    cc = u["contributionsCollection"]
    years = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))).days / 365.25
    stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
    commits = cc["totalCommitContributions"] + cc.get("restrictedContributionsCount", 0)
    return [
        ("Commits", commits, "past year", [1, 100, 500, 1000]),
        ("Repositories", u["repositories"]["totalCount"], "owned", [1, 10, 30, 50]),
        ("Pull Requests", u["pullRequests"]["totalCount"], "opened", [1, 10, 50, 200]),
        ("Stars", stars, "earned", [1, 10, 50, 200]),
        ("Followers", u["followers"]["totalCount"], "on GitHub", [1, 10, 50, 200]),
        ("Experience", round(years, 1), "years on GitHub", [0.5, 2, 5, 8]),
    ]


CUP = ("M-14,-17 h28 v9 a14,14 0 0 1 -11,13.6 v6.4 h7 v5 h-20 v-5 h7 v-6.4 a14,14 0 0 1 -11,-13.6 z "
       "M-14,-14 h-6 a6,6 0 0 0 6,8.5 z M14,-14 h6 a6,6 0 0 1 -6,8.5 z")


def fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    return f"{v / 1000:.1f}".rstrip("0").rstrip(".") + "k" if v >= 1000 else str(v)


def trophies_svg(cards, p):
    gap, h = 12, 172
    cw = (CARD_W - gap * (len(cards) - 1)) / len(cards)
    fill_for = {"S": "url(#gS)", "A": p["a2"], "B": p["a1"], "C": p["muted"], "?": p["dim"]}
    defs = (f'<linearGradient id="gS" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{p["a1"]}"/>'
            f'<stop offset=".5" stop-color="{p["a2"]}"/><stop offset="1" stop-color="{p["a3"]}"/></linearGradient>')
    body = []
    for i, (title, value, sub, th) in enumerate(cards):
        r = rank(value, th)
        x = PAD + i * (cw + gap)
        cx = x + cw / 2
        f = fill_for[r]
        body.append(
            f'<rect x="{x + .5:.1f}" y="1.5" width="{cw - 1:.1f}" height="{h - 3}" rx="12" fill="{p["card"]}" stroke="{p["border"]}"/>'
            f'<g transform="translate({cx:.1f},44)"><path d="{CUP}" fill="{f}" fill-rule="evenodd"/>'
            f'<text y="-5" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{p["card"]}">{r}</text></g>'
            f'<text x="{cx:.1f}" y="96" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{p["heading"]}">{escape(title)}</text>'
            f'<text x="{cx:.1f}" y="125" text-anchor="middle" font-family="{MONO}" font-size="20" font-weight="500" fill="{f if r != "?" else p["dim"]}">{fmt(value)}</text>'
            f'<text x="{cx:.1f}" y="148" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="500" fill="{p["dim"]}">{escape(sub)}</text>')
    label = ", ".join(f"{t} {fmt(v)} (rank {rank(v, th)})" for t, v, _, th in cards)
    return svg_doc(h, f"GitHub trophies: {label}", "".join(body), defs)


def placeholder_svg(h, text, p):
    body = (f'<rect x="{PAD + .5}" y="1.5" width="{CARD_W - 1}" height="{h - 3}" rx="12" fill="{p["card"]}" stroke="{p["border"]}"/>'
            f'<text x="{W / 2}" y="{h / 2 + 4}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="500" '
            f'fill="{p["muted"]}">{escape(text)}</text>')
    return svg_doc(h, text, body)


def write(name, content):
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("wrote", name)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    if "--seed" in sys.argv:
        for prefix, themes in PALETTES.items():
            for theme, p in themes.items():
                write(f"{prefix}activity-{theme}.svg", placeholder_svg(300, "Activity graph appears after the “Update profile cards” workflow runs", p))
                write(f"{prefix}trophies-{theme}.svg", placeholder_svg(172, "Trophies appear after the “Update profile cards” workflow runs", p))
        return
    if "--mock" in sys.argv:
        u = json.load(open(sys.argv[sys.argv.index("--mock") + 1]))
    else:
        u = fetch()
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days = [d for d in days if dt.date.fromisoformat(d["date"]) <= dt.datetime.now(dt.timezone.utc).date()]
    private_note = "" if TOKEN.startswith(("ghp_", "github_pat_")) or "--mock" in sys.argv else " (public)"
    cards = trophy_cards(u)
    for prefix, themes in PALETTES.items():
        for theme, p in themes.items():
            write(f"{prefix}activity-{theme}.svg", activity_svg(days, cal["totalContributions"], p, private_note))
            write(f"{prefix}trophies-{theme}.svg", trophies_svg(cards, p))


if __name__ == "__main__":
    main()
