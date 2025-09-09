
import subprocess, sys

def run(cmd):
    print(f"→ Running: {cmd}", flush=True)
    res = subprocess.run([sys.executable, "-u"] + cmd.split(), check=True)
    return res.returncode

if __name__ == "__main__":
    run("ingest_platforms.py")
    run("ingest_games.py")
    run("update_prices.py")
