import sys, subprocess, re, statistics as stats
# === Agent name from command line ===
if len(sys.argv) < 2:
    print("Usage: python3 experiments/runner.py <AgentName> [games_per_layout]")
    print("Example: python3 experiments/runner.py PacmanDQN 20")
    sys.exit(1)

agent = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20  # default 20 games

layouts = [
    "capsuleClassic","contestClassic","mediumClassic","minimaxClassic",
    "openClassic","originalClassic","powerClassic","smallClassic",
    "testClassic","trappedClassic","trickyClassic"
]

N = 20  # games per layout
agent = "PacmanDQN"

rx_score = re.compile(r"Average Score:\s*([-\d\.]+)")
rx_win   = re.compile(r"Win Rate:\s*(\d+)/(\d+)")

rows = []
for L in layouts:
    print(f"\n=== {L} ===")
    proc = subprocess.run(
        ["python","pacman.py","-p",agent,"-l",L,"-n",str(N),"-q"],
        capture_output=True, text=True
    )
    out = proc.stdout + proc.stderr
    avg_score = float(rx_score.search(out).group(1)) if rx_score.search(out) else float("nan")
    m = rx_win.search(out)
    wins, total = (int(m.group(1)), int(m.group(2))) if m else (0, N)
    winrate = wins / total if total else 0.0
    rows.append((L, winrate, avg_score))
    print(out)

# Rank by hardest (lowest win rate, then lower score)
rows.sort(key=lambda x: (x[1], x[2]))
print("\n=== Ranked (hardest → easiest) ===")
for L, wr, sc in rows:
    print(f"{L:16s}  win%={wr*100:5.1f}   avg_score={sc:8.1f}")

