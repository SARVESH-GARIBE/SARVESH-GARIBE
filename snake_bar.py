# Replaces the snake's chunky bottom bar with a thin dotted line + moving glowing dot.
import re, sys

for path in sys.argv[1:]:
    s = open(path).read()
    dark = "dark" in path
    bars = re.findall(r'<rect class="u [^"]*"[^>]*/>', s)
    if not bars:
        print("no bar found in", path); continue
    y = float(re.search(r'y="([\d.]+)"', bars[0]).group(1))
    h = float(re.search(r'height="([\d.]+)"', bars[0]).group(1))
    xs = [(float(re.search(r'x="([\d.]+)"', b).group(1)), float(re.search(r'width="([\d.]+)"', b).group(1))) for b in bars]
    x0 = min(x for x, _ in xs); x1 = max(x + w for x, w in xs)
    cy = y + h / 2
    dur = int(re.search(r'animation:\s*none linear (\d+)ms', s).group(1))
    eats = sorted(float(m) for m in re.findall(r'@keyframes c[0-9a-z]+\{([\d.]+)%', s))
    n = len(eats)
    pts = [(0.0, 0.0)] + [(eats[min(n-1, int(i*n/40))], min(n, int(i*n/40)+1)/n) for i in range(40)] + [(eats[-1], 1.0)]
    end = min(99.0, eats[-1] + 1.5)
    kp = "".join(f"{t:.2f}%{{transform:scaleX({f:.3f})}}" for t, f in pts) + f"{end:.2f}%{{transform:scaleX(1);opacity:1}}100%{{transform:scaleX(1);opacity:0}}"
    kh = "".join(f"{t:.2f}%{{transform:translateX({f*(x1-x0):.1f}px)}}" for t, f in pts) + f"{end:.2f}%{{transform:translateX({x1-x0:.1f}px);opacity:1}}100%{{transform:translateX({x1-x0:.1f}px);opacity:0}}"
    for b in bars:
        s = s.replace(b, "")

    track = "#30363d" if dark else "#d0d7de"
    line = "#7ee787" if dark else "#1a7f37"
    head = "#e6edf3" if dark else "#1f2328"

    style = f"""
.bt{{stroke:{track};stroke-width:2;stroke-linecap:round;stroke-dasharray:0 8}}
.bp{{stroke:{line};stroke-width:1.5;transform-origin:{x0}px {cy}px;animation:bp {dur}ms linear infinite}}
.bh{{fill:{head};animation:bh {dur}ms linear infinite}}
.bg{{fill:{line};opacity:.35;animation:bh {dur}ms linear infinite,bg 1.2s ease-in-out infinite}}
@keyframes bp{{{kp}}}
@keyframes bh{{{kh}}}
@keyframes bg{{50%{{opacity:.08}}}}
"""
    els = (f'<line class="bt" x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}"/>'
           f'<line class="bp" x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}"/>'
           f'<g class="bg"><circle cx="{x0}" cy="{cy}" r="6"/></g>'
           f'<g class="bh"><circle cx="{x0}" cy="{cy}" r="2.5"/></g>')
    s = s.replace("</style>", style + "</style>", 1)
    s = s.replace("</svg>", els + "</svg>")
    open(path, "w").write(s)
    print("updated", path)
